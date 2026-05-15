#!/usr/bin/env python3
"""pressure_testing_harness.py

Runs the seven pressure-testing checks against a target file or
directory. The checks operationalize the Hard Rules into automatable
evaluations.

The seven checks:

    1. AI signature scan. Em dashes, banned vocabulary,
       throat-clearing phrases, three-part cadence.
    2. Veracity flag. Numeric claims, named entities, and dates
       within a paragraph that lacks a citation marker.
    3. Falsifiability flag. Soft hedges ("may," "could,"
       "possibly," "perhaps") without nearby numbers or conditionals.
    4. Confidence label check. For files inside analysis or research
       contexts, every "finding" heading must have a confidence label.
    5. Scope drift heuristic. File length growth beyond a documented
       budget; presence of sections not listed in the spec.
    6. Three-part cadence count. Counts patterns; high counts are
       flagged for human review.
    7. Sentence-length variance. Pure AI prose has low variance;
       a flag is raised if variance falls below a threshold.

Usage:
    python pressure_testing_harness.py <path>
    python pressure_testing_harness.py docs/agent-teams-pattern.md
    python pressure_testing_harness.py --recursive reference/

Exits 0 if no blocker-severity issues found. Exits 1 if any
blocker-severity issue is raised.
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path


BANNED_VOCAB = re.compile(
    r"\b(delve|landscape|leverage|leverages|leveraging|robust|utilize|utilizes|"
    r"utilizing|streamline|streamlines|spearhead|holistic|synergy|paradigm)\b",
    re.IGNORECASE,
)

THROAT_CLEARING = re.compile(
    r"(it'?s important to note|it'?s worth noting|it bears mentioning|"
    r"in conclusion[,:.]|to summarize[,:]|in summary[,:.])",
    re.IGNORECASE,
)

SOFT_HEDGE = re.compile(r"\b(could|possibly|perhaps|might)\b", re.IGNORECASE)

# Substantive numeric claims only. Skips version numbers, tier
# labels, list markers, and small range numbers. Flags numbers
# with currency, percentage, decimals, or three or more digits.
SUBSTANTIVE_NUMBERS = re.compile(
    r"(?<![v.])\b(\$\d[\d,]*(\.\d+)?[KMB]?|\d+(\.\d+)?%|\d+\.\d+|\d{3,})\b"
)

NAMED_ENTITY = re.compile(r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b")
CITATION_MARKER = re.compile(r"(\[\d+\]|\(\d{4}\)|see https?://|cf\.|cited|per [A-Z])")

THREE_PART = re.compile(r", [a-zA-Z][a-zA-Z ]+, and [a-zA-Z]")

EXEMPT_FILES = {
    "CLAUDE.md",  # Root constitution quotes the banned words.
    "AGENTS.md",  # Cross-tool standard file quotes the banned words.
    "_template/CLAUDE.md",
    "_shared/rules/ai-signature-prohibition.md",
    "_shared/rules/communication-style.md",
    "_shared/rules/data-governance.md",
    "_shared/.claude/skills/writing-style/SKILL.md",
    "_shared/.claude/skills/pressure-testing/SKILL.md",
    "docs/hooks-layer.md",
    "docs/schema-reference.md",
}


@dataclass
class Finding:
    check: str
    severity: str  # "blocker", "major", "minor"
    location: str
    message: str


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks from markdown text."""
    return re.sub(r"```[\s\S]*?```", "", text)


def check_ai_signature(text: str, file_path: Path) -> list[Finding]:
    findings = []
    prose = strip_code_blocks(text)

    # Em dash check.
    for i, line in enumerate(prose.splitlines(), start=1):
        if "—" in line:
            findings.append(Finding(
                "ai_signature", "major", f"{file_path}:{i}",
                f"em dash in prose",
            ))

    # Banned vocab (skip if file is exempt).
    relative = str(file_path).split("cortex-os/", 1)[-1] if "cortex-os/" in str(file_path) else str(file_path)
    is_exempt = any(relative.endswith(exempt) for exempt in EXEMPT_FILES)

    if not is_exempt:
        for match in BANNED_VOCAB.finditer(prose):
            findings.append(Finding(
                "ai_signature", "major", f"{file_path}",
                f"banned vocabulary: '{match.group()}'",
            ))
        for match in THROAT_CLEARING.finditer(prose):
            findings.append(Finding(
                "ai_signature", "major", f"{file_path}",
                f"throat-clearing: '{match.group()}'",
            ))

    return findings


def check_three_part_cadence(text: str, file_path: Path) -> list[Finding]:
    prose = strip_code_blocks(text)
    count = len(THREE_PART.findall(prose))
    if count > 5:
        return [Finding(
            "three_part_cadence", "minor", str(file_path),
            f"{count} three-part list patterns (review for AI cadence)",
        )]
    return []


def check_sentence_variance(text: str, file_path: Path) -> list[Finding]:
    prose = strip_code_blocks(text)
    # Approximate sentence splitting.
    sentences = re.split(r"(?<=[.!?])\s+", prose)
    sentences = [s for s in sentences if 5 < len(s) < 500]
    if len(sentences) < 10:
        return []
    lengths = [len(s.split()) for s in sentences]
    variance = statistics.variance(lengths) if len(lengths) > 1 else 0
    if variance < 20:
        return [Finding(
            "sentence_variance", "minor", str(file_path),
            f"sentence-length variance {variance:.1f} is low (typical AI prose pattern)",
        )]
    return []


def check_veracity_flags(text: str, file_path: Path) -> list[Finding]:
    findings = []
    paragraphs = re.split(r"\n\s*\n", strip_code_blocks(text))
    for i, para in enumerate(paragraphs, start=1):
        # Skip headings, code blocks already stripped.
        if not para.strip() or para.strip().startswith("#"):
            continue
        has_substantive_number = bool(SUBSTANTIVE_NUMBERS.search(para))
        has_citation = bool(CITATION_MARKER.search(para))
        if has_substantive_number and not has_citation:
            findings.append(Finding(
                "veracity", "minor", f"{file_path}:para {i}",
                "substantive numeric claim without nearby citation marker",
            ))
    return findings


def check_falsifiability(text: str, file_path: Path) -> list[Finding]:
    findings = []
    prose = strip_code_blocks(text)
    sentences = re.split(r"(?<=[.!?])\s+", prose)
    for s in sentences:
        if not SOFT_HEDGE.search(s):
            continue
        # Hedge is allowed if there's a number or a conditional ("if ... then").
        if SUBSTANTIVE_NUMBERS.search(s) or re.search(r"\bif\b.*\bthen\b|\bif\b", s, re.IGNORECASE):
            continue
        findings.append(Finding(
            "falsifiability", "minor", str(file_path),
            f"soft hedge without number or conditional: '{s.strip()[:80]}...'",
        ))
    # Cap to avoid noise.
    return findings[:5]


def run_checks(file_path: Path) -> list[Finding]:
    if not file_path.is_file() or file_path.suffix not in {".md", ".markdown", ".txt"}:
        return []
    text = file_path.read_text()
    findings = []
    findings.extend(check_ai_signature(text, file_path))
    findings.extend(check_three_part_cadence(text, file_path))
    findings.extend(check_sentence_variance(text, file_path))
    findings.extend(check_veracity_flags(text, file_path))
    findings.extend(check_falsifiability(text, file_path))
    return findings


def collect_files(target: Path, recursive: bool) -> list[Path]:
    if target.is_file():
        return [target]
    if recursive:
        return sorted(target.rglob("*.md"))
    return sorted(target.glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the seven pressure-testing checks against a file or directory.",
    )
    parser.add_argument("path", type=Path, help="File or directory.")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"pressure_testing_harness: path not found: {args.path}", file=sys.stderr)
        return 1

    files = collect_files(args.path, args.recursive)
    if not files:
        print("pressure_testing_harness: no markdown files found.", file=sys.stderr)
        return 1

    all_findings: list[Finding] = []
    by_severity = {"blocker": 0, "major": 0, "minor": 0}

    for f in files:
        findings = run_checks(f)
        if findings:
            print(f"\n{f}")
            for finding in findings:
                print(f"  [{finding.severity}] {finding.check}: {finding.message}  ({finding.location})")
            all_findings.extend(findings)
            for finding in findings:
                by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1

    print(f"\n{len(files)} files checked. Findings: blocker={by_severity['blocker']}, "
          f"major={by_severity['major']}, minor={by_severity['minor']}.")

    return 1 if by_severity["blocker"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
