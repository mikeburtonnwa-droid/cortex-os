# Cortex-OS

A cascading constitutional architecture for AI operating systems built on Claude Code's native primitives. Cortex-OS is not a framework to install. It is a pattern to fork, adapt, and inhabit.

```
       Root constitution (CLAUDE.md)
                  │
        ┌─────────┼─────────┐
   Domain     Business     Function
                  │
              Environment

   Cascading config           Deterministic hooks
   ─────────────────         ──────────────────
   loaded by Claude Code      fire on lifecycle events
   walks the directory tree   block or allow tool calls
   deeper files refine        enforce voice, scope, safety
```

Four layers compose the pattern:

1. **Cascading CLAUDE.md constitutions.** Root, domain, business, function, environment. Each level refines the one above. The cascade is the authority for what rules apply in a given context.
2. **Deterministic hooks.** PreToolUse, PostToolUse, Stop, PreCompact. Bash scripts that fire on Claude Code lifecycle events and enforce rules that cannot be left to the model's discretion.
3. **Agent teams with context-boundary discipline.** Hub-and-spoke orchestration where each specialist agent sees only what its role requires. Independence is enforced, not advisory.
4. **Schema-driven configuration.** Agent frontmatter, models.yaml, tools.yaml, settings.json. Routing, permissions, and failure protocols are declared, not inferred.

## Why this exists

Most "Claude system prompts" stop at Level 5 on the developer-AI evolution scale described by Steve Yegge and Gene Kim. Operators write a long prompt, then hope the model follows it. Cortex-OS targets Level 6+ orchestration: hierarchical context that loads itself, deterministic enforcement that catches what advisory rules miss, multi-agent teams with context boundaries that prevent groupthink, and schema-driven configuration that validates before runtime rather than failing during it.

The repository contains the pattern, a fully-instantiated reference business (ResearchCo) that demonstrates the cascade in action, and six runtime scripts that let an operator verify the cascade resolves, the schemas validate, and the hooks fire on a fresh clone.

## Quick navigation

- [QUICKSTART.md](QUICKSTART.md) – thirty-minute path from fork to first working session
- [ARCHITECTURE.md](ARCHITECTURE.md) – technical deep dive on the four layers
- [docs/](docs/) – per-layer references (cascade pattern, hooks layer, agent teams, schemas)
- [_template/](_template/) – blank templates to copy into your own project
- [reference/business-example/](reference/business-example/) – ResearchCo, the worked example
- [runtime/](runtime/) – inspection and validation utilities
- [CONTRIBUTING.md](CONTRIBUTING.md) – contribution standards

## Status

Initial public release. The pattern is stable. The reference business and runtime layer are complete. A companion repository will publish the production execution pattern (LangGraph + Temporal wrapping a Cortex-OS-governed workflow) following community engagement on this one.

## License and attribution

MIT License. See [LICENSE](LICENSE).

The vibe coding evolution model that frames "Level 6+" is from Steve Yegge and Gene Kim's writing on AI-augmented engineering. The Agent Teams primitive and Claude Code are Anthropic's. Skills, hook patterns, and schema conventions referenced here build on community work that predates this repository.

For citation in academic or professional work, see [CITATION.cff](CITATION.cff).

Maintained by Michael Burton. Issues and pull requests welcome under the standards described in CONTRIBUTING.md.
