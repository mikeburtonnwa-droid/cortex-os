# AGENTS.md

This repository follows the Cortex-OS pattern: an opinionated reference implementation that composes Claude Code's native primitives into a disciplined operating system.

For agentic tools that read AGENTS.md under the Linux Foundation Agentic AI Foundation standard (Codex, Copilot, Cursor, Windsurf, Amp, Devin, others), the canonical operating constitution lives at `CLAUDE.md` at the repository root.

## Read this first

`CLAUDE.md` at the project root. Then walk the cascade for the working directory you are in:

- `CLAUDE.md` (root identity, hard rules, AI signature prohibition)
- `reference/business-example/CLAUDE.md` (for work in that subtree)
- `reference/business-example/functions/<name>/CLAUDE.md` (for work in those subtrees)

The cascade is hierarchical. Deeper files refine shallower ones. The cascade is monotonically restrictive as it descends.

## Hard rules that apply to every agent in this repository

Direct, declarative output. Lead with the answer; evidence follows.

No em dashes in prose. Use commas, semicolons, periods, or en dashes.

No banned vocabulary: delve, landscape, leverage, robust, utilize, streamline, spearhead, holistic, synergy, paradigm. See `_shared/rules/ai-signature-prohibition.md` for substitutions.

No throat-clearing phrases: "it's important to note," "in conclusion," "to summarize," and variants.

No three-part list cadence unless the content genuinely has three parts.

Veracity is non-negotiable. No hallucinated citations, dates, or data.

## Pattern in 60 seconds

Four layers compose the system:

1. Cascading CLAUDE.md constitutions, loaded by Claude Code as you walk the directory tree.
2. Deterministic bash hooks at `_shared/.claude/hooks/` (PreToolUse, PostToolUse, Stop, PreCompact).
3. Hub-and-spoke agent teams at `reference/agents/` with enforced context boundaries.
4. Schema-driven configuration at `_template/` and `reference/business-example/`, validated by Python scripts at `runtime/`.

The validation tooling at `runtime/` is the strongest differentiator of this reference. Run `python runtime/cascade_walker.py <path>` to see what loads for any working directory. Run `python runtime/schema_validator.py --recursive .` to validate every agent definition, models.yaml, tools.yaml, and settings.json. Run `python runtime/pressure_testing_harness.py --recursive .` to scan markdown for AI signature violations and other quality checks.

## Tool-specific notes

If you are a tool that does not support Claude Code's hook primitives (PreToolUse, PostToolUse, Stop, PreCompact), you cannot enforce the AI signature prohibition deterministically. The rules still apply; enforce them via your own conventions or pre-commit hooks.

If you are a tool that does not load CLAUDE.md hierarchically, read this AGENTS.md plus `CLAUDE.md` at the root, and treat the function-level constitutions under `reference/business-example/functions/*/CLAUDE.md` as scope-specific overrides when working in those subtrees.

## Contributing

See `CONTRIBUTING.md`. Pull requests require pressure-testing via `runtime/pressure_testing_harness.py` and must conform to the schemas validated by `runtime/schema_validator.py`. Pattern additions require an approved issue first.

## License

MIT. See `LICENSE`.
