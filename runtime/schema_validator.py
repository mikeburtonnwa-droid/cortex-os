#!/usr/bin/env python3
"""schema_validator.py

Validates Cortex-OS configuration files against the documented schemas
in docs/schema-reference.md.

Supports four file types:

    1. Agent definition files (markdown with YAML frontmatter)
    2. models.yaml
    3. tools.yaml
    4. settings.json

Usage:
    python schema_validator.py <path>
    python schema_validator.py reference/agents/orchestrator.md
    python schema_validator.py reference/business-example/tools.yaml
    python schema_validator.py --recursive reference/

Exits 0 if all files are valid, 1 if any file has violations.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    print("schema_validator: PyYAML is required. Install with: pip install PyYAML", file=sys.stderr)
    sys.exit(1)


# ----- Schema definitions -----

AGENT_FIELDS = {
    "name": {"type": str, "required": True},
    "description": {"type": str, "required": True},
    "model": {"type": str, "required": True, "allowed": ["opus", "sonnet", "haiku"]},
    "tools": {"type": list, "required": False},
    "disallowedTools": {"type": list, "required": False},
    "permissionMode": {"type": str, "required": False, "allowed": ["ask", "auto", "deny"]},
    "maxTurns": {"type": int, "required": False, "range": (1, 100)},
    "skills": {"type": list, "required": False},
    "mcpServers": {"type": list, "required": False},
    "hooks": {"type": list, "required": False},
    "memory": {"type": str, "required": False, "allowed": ["short", "long", "none"]},
    "background": {"type": str, "required": False},
}

TOOLS_FAILURE_PROTOCOLS = {"retry", "escalate", "halt", "log_and_continue"}
TOOLS_TYPES = {"native", "mcp", "bash", "custom"}


@dataclass
class Violation:
    file: Path
    field: str
    message: str


@dataclass
class ValidationResult:
    file: Path
    violations: list[Violation] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.violations) == 0


# ----- Frontmatter parsing -----

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error: {e}")


# ----- Validators -----

def validate_agent(file_path: Path) -> ValidationResult:
    result = ValidationResult(file=file_path)
    text = file_path.read_text()

    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as e:
        result.violations.append(Violation(file_path, "frontmatter", str(e)))
        return result

    if frontmatter is None:
        result.violations.append(Violation(
            file_path, "frontmatter",
            "No YAML frontmatter found. Agent files must begin with '---\\n<yaml>\\n---'.",
        ))
        return result

    for field_name, spec in AGENT_FIELDS.items():
        if spec["required"] and field_name not in frontmatter:
            result.violations.append(Violation(
                file_path, field_name,
                f"Required field is missing.",
            ))
            continue
        if field_name not in frontmatter:
            continue
        value = frontmatter[field_name]
        if not isinstance(value, spec["type"]):
            result.violations.append(Violation(
                file_path, field_name,
                f"Expected {spec['type'].__name__}, got {type(value).__name__}.",
            ))
            continue
        if "allowed" in spec and value not in spec["allowed"]:
            result.violations.append(Violation(
                file_path, field_name,
                f"Value '{value}' not in allowed set {spec['allowed']}.",
            ))
        if "range" in spec:
            low, high = spec["range"]
            if not (low <= value <= high):
                result.violations.append(Violation(
                    file_path, field_name,
                    f"Value {value} outside allowed range [{low}, {high}].",
                ))

    # Detect unknown fields.
    for key in frontmatter:
        if key not in AGENT_FIELDS:
            result.violations.append(Violation(
                file_path, key,
                f"Unknown field. Not in documented schema.",
            ))

    return result


def validate_models_yaml(file_path: Path) -> ValidationResult:
    result = ValidationResult(file=file_path)
    try:
        data = yaml.safe_load(file_path.read_text())
    except yaml.YAMLError as e:
        result.violations.append(Violation(file_path, "yaml", str(e)))
        return result

    if not isinstance(data, dict) or "roles" not in data:
        result.violations.append(Violation(
            file_path, "structure",
            "models.yaml must have a top-level 'roles' key.",
        ))
        return result

    roles = data["roles"]
    if not isinstance(roles, dict):
        result.violations.append(Violation(
            file_path, "roles",
            "'roles' must be a mapping of role_name to role_config.",
        ))
        return result

    for role_name, role_config in roles.items():
        if not isinstance(role_config, dict):
            result.violations.append(Violation(
                file_path, f"roles.{role_name}",
                "Role config must be a mapping.",
            ))
            continue
        if "model" not in role_config:
            result.violations.append(Violation(
                file_path, f"roles.{role_name}.model",
                "Required key 'model' missing.",
            ))
        elif role_config["model"] not in {"opus", "sonnet", "haiku"} and not str(role_config["model"]).startswith("claude-"):
            result.violations.append(Violation(
                file_path, f"roles.{role_name}.model",
                f"Unrecognized model: {role_config['model']}.",
            ))

    return result


def validate_tools_yaml(file_path: Path) -> ValidationResult:
    result = ValidationResult(file=file_path)
    try:
        data = yaml.safe_load(file_path.read_text())
    except yaml.YAMLError as e:
        result.violations.append(Violation(file_path, "yaml", str(e)))
        return result

    if not isinstance(data, dict) or "tools" not in data:
        result.violations.append(Violation(
            file_path, "structure",
            "tools.yaml must have a top-level 'tools' key.",
        ))
        return result

    tools = data["tools"]
    if not isinstance(tools, dict):
        result.violations.append(Violation(
            file_path, "tools",
            "'tools' must be a mapping.",
        ))
        return result

    for tool_name, tool_config in tools.items():
        if not isinstance(tool_config, dict):
            result.violations.append(Violation(
                file_path, f"tools.{tool_name}",
                "Tool config must be a mapping.",
            ))
            continue

        tool_type = tool_config.get("type")
        if tool_type not in TOOLS_TYPES:
            result.violations.append(Violation(
                file_path, f"tools.{tool_name}.type",
                f"Type '{tool_type}' not in {sorted(TOOLS_TYPES)}.",
            ))

        if tool_type == "mcp" and "server" not in tool_config:
            result.violations.append(Violation(
                file_path, f"tools.{tool_name}.server",
                "type=mcp requires a 'server' field.",
            ))

        on_failure = tool_config.get("on_failure")
        if on_failure not in TOOLS_FAILURE_PROTOCOLS:
            result.violations.append(Violation(
                file_path, f"tools.{tool_name}.on_failure",
                f"on_failure '{on_failure}' not in {sorted(TOOLS_FAILURE_PROTOCOLS)}.",
            ))

    return result


def validate_settings_json(file_path: Path) -> ValidationResult:
    result = ValidationResult(file=file_path)
    try:
        data = json.loads(file_path.read_text())
    except json.JSONDecodeError as e:
        result.violations.append(Violation(file_path, "json", str(e)))
        return result

    # Light validation: hooks section structure and known keys.
    if "hooks" in data:
        for event_name, event_config in data["hooks"].items():
            if event_name not in {"PreToolUse", "PostToolUse", "Stop", "PreCompact", "UserPromptSubmit", "SubagentStop"}:
                result.violations.append(Violation(
                    file_path, f"hooks.{event_name}",
                    f"Unknown hook event.",
                ))

    return result


# ----- Dispatch -----

def validate_file(file_path: Path) -> ValidationResult | None:
    name = file_path.name
    if name.endswith(".md") and "agents/" in str(file_path):
        return validate_agent(file_path)
    if name == "models.yaml":
        return validate_models_yaml(file_path)
    if name == "tools.yaml":
        return validate_tools_yaml(file_path)
    if name == "settings.json":
        return validate_settings_json(file_path)
    return None


def collect_files(target: Path, recursive: bool) -> list[Path]:
    if target.is_file():
        return [target]
    if not recursive:
        return []
    files = []
    for ext_pattern in ("**/*.md", "**/models.yaml", "**/tools.yaml", "**/settings.json"):
        files.extend(target.glob(ext_pattern))
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Cortex-OS config files against documented schemas.",
    )
    parser.add_argument("path", type=Path, help="File or directory to validate.")
    parser.add_argument("--recursive", action="store_true", help="Validate all matching files under a directory.")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"schema_validator: path not found: {args.path}", file=sys.stderr)
        return 1

    files = collect_files(args.path, args.recursive)
    if not files and args.path.is_file():
        files = [args.path]

    if not files:
        print(f"schema_validator: no validatable files found at {args.path}.", file=sys.stderr)
        return 1

    all_violations: list[Violation] = []
    checked = 0
    for f in files:
        result = validate_file(f)
        if result is None:
            continue
        checked += 1
        if result.violations:
            print(f"\nFAIL: {result.file}")
            for v in result.violations:
                print(f"  - {v.field}: {v.message}")
            all_violations.extend(result.violations)
        else:
            print(f"PASS: {result.file}")

    print(f"\n{checked} files validated. {len(all_violations)} violations.")
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
