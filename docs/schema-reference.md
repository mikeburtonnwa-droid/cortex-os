# Schema Reference

Cortex-OS uses three schemas to govern agent behavior, model routing, and tool access. This document specifies the canonical shape of each. The runtime layer (`runtime/`) validates files against these schemas; the constitutional layer (`CLAUDE.md`) cannot.

## 1. Agent Frontmatter Schema

Agent definition files live as markdown with YAML frontmatter. The frontmatter governs runtime selection. The body of the file is freeform guidance prepended to the agent's system prompt.

Twelve fields. Some map to Claude Code's native subagent fields; others are Cortex-OS extensions that the runtime layer parses and applies.

### `name`

- **Type:** string
- **Allowed values:** lowercase letters, digits, hyphens. Must be unique within the project.
- **Default:** none (required)
- **When to set it:** Always. The name is how other agents and the orchestrator address this agent.

### `description`

- **Type:** string (one to three sentences)
- **Allowed values:** any prose
- **Default:** none (required)
- **When to set it:** Always. The description is what the auto-invocation matcher reads when deciding whether to load this agent for a given prompt. Write it as if you were telling another agent when to delegate.

### `model`

- **Type:** string enum
- **Allowed values:** `opus`, `sonnet`, `haiku`. Specific model strings (e.g., `claude-opus-4-6`) are also accepted and override the alias.
- **Default:** `sonnet`
- **When to set it:** Set `opus` for agents that do complex reasoning or adversarial review. Set `sonnet` for general work. Set `haiku` for high-throughput, low-stakes tasks like routing or classification.

### `tools`

- **Type:** list of strings
- **Allowed values:** any tool name available in the parent Claude Code project
- **Default:** all tools the parent has access to
- **When to set it:** When the agent should be restricted to a narrow toolset. An analyst that should only read, never write, gets `[Read, Grep, Glob, WebSearch]`. Restricting tools is a stronger control than instructing the model not to use them.

### `disallowedTools`

- **Type:** list of strings
- **Allowed values:** any tool name
- **Default:** empty
- **When to set it:** When the agent inherits a broad toolset but specific tools must be excluded. Use this when the inverted list (`tools`) would be unwieldy.

### `permissionMode`

- **Type:** string enum
- **Allowed values:** `ask`, `auto`, `deny`
- **Default:** `ask`
- **When to set it:** Set `auto` for agents operating in a trusted sandbox where every tool call should proceed without prompt. Set `deny` for read-only review agents that should never modify state. Set `ask` for any agent that may touch production data or external systems.

### `maxTurns`

- **Type:** integer
- **Allowed values:** 1 to 100
- **Default:** 25
- **When to set it:** Lower this for narrow agents that should produce one output and stop. Raise it for orchestrators that coordinate multiple sub-tasks. A reviewer agent that runs once should have `maxTurns: 1`.

### `skills`

- **Type:** list of strings
- **Allowed values:** any skill identifier known to the project
- **Default:** empty (no skills pre-loaded)
- **When to set it:** When the agent should always have certain skills loaded regardless of auto-invocation. A writer agent always loads `writing-style` and `voice-guide`. Skills not listed here may still load via auto-invocation.

### `mcpServers`

- **Type:** list of strings
- **Allowed values:** any MCP server identifier configured in `settings.json`
- **Default:** all servers configured at the project level
- **When to set it:** When the agent should connect to a subset of MCP servers. A researcher that needs web access but not the company's CRM gets `[web-search]` only.

### `hooks`

- **Type:** list of strings
- **Allowed values:** hook script names available under `.claude/hooks/`
- **Default:** all hooks configured at the project level
- **When to set it:** When an agent should run with a custom hook set. Typically left default; override only for agents that operate under different enforcement rules.

### `memory`

- **Type:** string enum
- **Allowed values:** `short`, `long`, `none`
- **Default:** `short`
- **When to set it:** `short` retains context within a session and drops it on stop. `long` persists context across sessions via the Current Reality block in the relevant CLAUDE.md. `none` is stateless per call. Use `long` for ongoing project work; `none` for atomic operations like classification.

### `background`

- **Type:** string
- **Allowed values:** prose describing the agent's persona, expertise, or operating context
- **Default:** empty
- **When to set it:** When the agent needs a stable identity beyond what the description conveys. Useful for review agents that should embody a specific reviewer archetype.

## 2. Models Routing Schema (`models.yaml`)

`models.yaml` declares which model serves which role. Agents reference roles in their frontmatter; the runtime resolves the role to a concrete model at invocation time.

```yaml
# Schema
roles:
  <role_name>:
    model: <opus | sonnet | haiku | specific-model-string>
    reasoning_effort: <minimal | low | medium | high>  # optional
    notes: <string>  # optional, freeform
```

The runtime walks the cascade for `models.yaml`: function-level overrides business-level overrides root-level. The deepest file wins.

## 3. Tools Configuration Schema (`tools.yaml`)

`tools.yaml` declares the project's tool inventory and per-tool failure protocols.

```yaml
# Schema
tools:
  <tool_name>:
    type: <native | mcp | bash | custom>
    server: <mcp_server_id>  # required if type=mcp
    on_failure: <retry | escalate | halt | log_and_continue>
    timeout_seconds: <integer>  # optional
    requires_approval: <true | false>
```

`on_failure` is the failure protocol the orchestrator follows when this tool errors. `retry` attempts the call again with the same parameters. `escalate` surfaces the error to the operator and pauses. `halt` stops the session. `log_and_continue` records the failure and proceeds with degraded output.

## 4. Settings Schema (`settings.json`)

`settings.json` wires hooks, permissions, and MCP servers to a Claude Code project. This file follows Claude Code's native settings format; the schema below documents the subset Cortex-OS templates use.

```json
{
  "hooks": {
    "PreToolUse": [{"hooks": [{"type": "command", "command": "<path>"}]}],
    "PostToolUse": [{"hooks": [{"type": "command", "command": "<path>"}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "<path>"}]}],
    "PreCompact": [{"hooks": [{"type": "command", "command": "<path>"}]}]
  },
  "permissions": {
    "allow": ["<tool_pattern>"],
    "deny": ["<tool_pattern>"]
  },
  "mcpServers": {
    "<server_id>": {
      "command": "<command>",
      "args": ["<arg>"],
      "env": {}
    }
  }
}
```

Hook command paths should be relative to the project root or absolute. Permission patterns follow Claude Code's tool-name matching rules.

## Validation

The schema validator at `runtime/schema_validator.py` (Phase 5R) parses any of the above files and reports violations. Validation is run on commit via the pressure-testing harness. Invalid schemas block the commit.
