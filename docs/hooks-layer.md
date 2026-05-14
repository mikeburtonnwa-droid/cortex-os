# The Hooks Layer

Cortex-OS has two control layers. Constitutional rules live in `CLAUDE.md` files and are advisory: the model reads them, agrees, and intends to follow. The hooks layer is deterministic: bash scripts that fire on defined events and either pass or block, regardless of what the model intended.

Both layers are necessary. CLAUDE.md gives the model context for *why* a rule exists. Hooks ensure the rule survives context pressure, prompt injection, and the long-session drift that degrades instruction-following.

## Master Principle: Hooks enforce, CLAUDE.md advises

Encode rules that must hold every time as hooks. Keep judgment-dependent rules in CLAUDE.md. A rule only in CLAUDE.md will be violated. A rule in a hook cannot be.

## The four hooks

**`pre-tool-use.sh`** fires before every tool call. It blocks tool calls whose parameters match sensitive-data patterns (API keys, AWS keys, `.env` references, private keys), blocks destructive bash commands (`rm -rf /`, fork bombs, raw writes to block devices), and blocks external-action tools (`send`, `post`, `publish`, `create_draft`) that lack an explicit `approved=true` parameter. Exits with code 2 to block; stderr surfaces to the model as feedback.

**`post-tool-use.sh`** fires after Write or Edit completes. It scans the new file content against the AI Signature Prohibition rules: em dashes in prose, banned vocabulary, throat-clearing phrases, three-part list cadence. Code blocks are exempt. Non-prose files are skipped. If a violation is found, the hook returns the file to the model with a specific correction.

**`stop.sh`** fires when the agent finishes a turn. It verifies the final assistant message contains a session summary (decided, built, changed, next) and re-runs the AI signature scan on the final output. If the summary is missing, the hook blocks termination and gives the model another turn to write it.

**`pre-compact.sh`** fires before Claude Code auto-compacts the session context window. It reads session state from `.claude/session-state.json` if present and emits a carry-forward block on stdout: current task, current phase, recently active files, and the non-negotiable constraints from the root constitution. This becomes part of the post-compaction context.

## Example

A model under context pressure calls a Gmail send tool without the approved flag. The pre-tool-use hook fires:

```
pre-tool-use: blocked. External-action tool send_email requires
approved=true in parameters.
```

The tool call is blocked. The model receives the stderr as feedback and surfaces the draft to the operator. CLAUDE.md advisory text can request this behavior. It cannot guarantee it.

## Where the hooks live

`_shared/.claude/hooks/`. Drop the `_shared/.claude/` directory into a Claude Code project root to activate them. Configure which events trigger which scripts in `.claude/settings.json` per the Claude Code hooks specification.

## What hooks cannot do

Hooks are bash scripts that exit with codes. They cannot rewrite content for the model; they can only block and feed back. They cannot enforce judgment-dependent rules ("is this analysis surface-level?") because they cannot read meaning. For those rules, the constitution and the pressure-testing protocol carry the load. Hooks handle the rules that have a deterministic answer.
