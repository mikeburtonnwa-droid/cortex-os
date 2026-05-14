# Runtime Layer

The runtime directory contains six standalone scripts that demonstrate Cortex-OS executes, not just configures. Each script has a single responsibility, reads from the filesystem (the source of truth), and reports its findings in a format a human can read.

The scripts require Python 3.9 or later and PyYAML. Install with `pip install PyYAML`.

## The six scripts

`cascade_walker.py` prints the cascade of CLAUDE.md files that would load for any given working directory. Walks up from the target path to the repository root, reporting each file in load order. Demonstrates the cascade is a real, traceable mechanism rather than a documentation concept.

```
python cascade_walker.py reference/business-example/functions/research/
```

`schema_validator.py` validates Cortex-OS config files against the schemas documented in `docs/schema-reference.md`. Handles four file types: agent definition files with YAML frontmatter, models.yaml, tools.yaml, and settings.json. Reports per-file pass or fail and itemizes every violation.

```
python schema_validator.py reference/ --recursive
```

`hook_simulator.py` runs a hook bash script against a JSON fixture and reports the exit code, stdout, and stderr. Lets an operator verify a hook fires correctly without a full Claude Code session in the loop.

```
python hook_simulator.py _shared/.claude/hooks/pre-tool-use.sh \
    runtime/fixtures/pretooluse_bash_destructive.json
```

`pressure_testing_harness.py` runs the seven pressure-testing checks against a target file or directory. The checks operationalize the Hard Rules: AI signature scan, veracity flag, falsifiability flag, confidence label check, scope drift heuristic, three-part cadence count, sentence-length variance. Reports findings by severity (blocker, major, minor).

```
python pressure_testing_harness.py --recursive docs/
```

`current_reality_updater.py` rewrites the Current Reality block in a CLAUDE.md file. Demonstrates the state-persistence pattern: durable session state lives in human-readable markdown rather than a database. Takes the new content from a file or stdin and replaces the block in place.

```
python current_reality_updater.py CLAUDE.md /tmp/session-end.md
```

`skill_invocation_simulator.py` simulates skill auto-invocation against a user prompt. Reads SKILL.md files from a directory, scores each against the prompt using keyword matching, and prints the ranked candidates with their matched terms. Not the same algorithm Claude Code uses internally; a transparent approximation that lets the operator see why a skill is or is not a candidate.

```
python skill_invocation_simulator.py "draft an outbound email" \
    _shared/.claude/skills/
```

## Why these scripts exist

A repository that documents a pattern is one thing. A repository that proves the pattern executes is another. The runtime layer is the difference between describing an operating system and shipping one.

Each script is intentionally short, intentionally standalone, and intentionally readable. A reader who wants to understand how the cascade resolves can read `cascade_walker.py` in under two minutes. A reader who wants to validate their own fork against the schemas can run `schema_validator.py --recursive` and get a per-file report. The scripts are the receipts for the claims in the documentation.

## Composition

The scripts compose cleanly. A pre-commit workflow that validates a fork before push looks like this:

```bash
python runtime/schema_validator.py --recursive .
python runtime/pressure_testing_harness.py --recursive docs/
python runtime/pressure_testing_harness.py --recursive reference/
```

A maintenance session that updates a CLAUDE.md with new state and then verifies the cascade still resolves:

```bash
python runtime/current_reality_updater.py CLAUDE.md /tmp/new-state.md
python runtime/cascade_walker.py reference/business-example/functions/research/
```

## What the runtime layer is not

The runtime layer is not a framework. It is six small scripts that happen to compose. There is no shared state, no installation step beyond `pip install PyYAML`, no central registry. Each script can be deleted and the others still work.

The runtime layer is not a replacement for Claude Code's native runtime. Claude Code reads CLAUDE.md files, fires hooks, and routes agents on its own. These scripts are inspection and validation utilities that operate on the same files Claude Code uses.

The runtime layer is not exhaustive. The seven pressure-testing checks are operationalizations of the Hard Rules; they catch the deterministic violations, not the judgment-dependent ones. A human reviewer still has work to do.
