# Template Setup

This directory holds blank templates for a new Cortex-OS deployment. Fork the repo, copy these files into a new project, replace the bracketed placeholders, and you have a working operating system.

## Files

`CLAUDE.md` is the root constitutional template. It defines who the operator is, what rules apply in every session, and how the cascade works. Replace every bracketed placeholder with operator-specific content. The Hard Rules section is published verbatim and should be modified only to add new rules, never to weaken existing ones.

`models.yaml` declares model routing. Roles map to specific Claude models. Agents reference roles in their frontmatter. Replace the example roles with the ones your project actually uses.

`tools.yaml` declares the tool inventory and per-tool failure protocols. Replace the example tools with the tools your project will call.

`settings.json` wires hooks, permissions, and MCP servers to Claude Code. The hook paths assume `_shared/.claude/hooks/` lives at the project root. Adjust if you place hooks elsewhere.

## Activation steps

1. Copy `CLAUDE.md` to your project root.
2. Copy `models.yaml`, `tools.yaml`, and `settings.json` to your project root or to `.claude/` per your preference. The runtime resolves both locations.
3. Copy `_shared/.claude/` from the cortex-os repo into your project to install the hook layer.
4. Replace bracketed placeholders in `CLAUDE.md` with operator-specific content.
5. Update `models.yaml` and `tools.yaml` to reflect your actual model and tool choices.
6. Run `runtime/cascade_walker.py` from the project root to verify the cascade resolves. The script will print the chain of CLAUDE.md files that load for any given working directory.
7. Run `runtime/schema_validator.py` against the project to verify every YAML and frontmatter file conforms to the documented schemas.

## Cascade rules

Claude Code loads CLAUDE.md files by walking up the directory tree from the current working directory. The deepest file is loaded last and conceptually overrides the shallower ones. Place specific overrides at deeper paths; place universal rules at the root.

## What this template does not include

The reference business at `reference/business-example/` is a separate, fully-instantiated example. It is not part of the blank template. Use it as a worked example when filling in your own templates.

The runtime scripts at `runtime/` are shared utilities for validation and inspection. They do not need to be copied; they run against the cortex-os repo itself.

## Verification

After completing the activation steps, run a Claude Code session in the project root and ask Claude to print its current operating context. The response should reference your root CLAUDE.md, confirm the cascade has loaded, and identify the current phase from your Current Reality block.

If any of those signals are absent, the cascade did not load. Re-check the file locations and run `runtime/cascade_walker.py` to diagnose.
