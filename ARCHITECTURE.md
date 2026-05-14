# Cortex-OS Architecture

Cortex-OS is a cascading declarative configuration system with event-driven enforcement and hub-and-spoke agent orchestration. It is not a graph runtime. The runtime is Claude Code; Cortex-OS layers context, control, and consistency on top.

Four layers compose the pattern. Two cross-cutting concerns (skill auto-invocation and pressure-testing) span all four. This document walks each in turn.

## 1. The cascade pattern

Cortex-OS treats CLAUDE.md files as a layered configuration system. Claude Code walks up the filesystem from the current working directory, collects every CLAUDE.md it finds, and loads them in order from shallowest to deepest. The deepest file wins on any point of contradiction.

Five levels are standard: root identity, domain, business, function, environment. Not every deployment uses all five. The reference business at `reference/business-example/` uses three (root, business, function); a more elaborate deployment uses all five.

Each level can add new rules, refine existing rules, or tighten them. Loosening rules at deeper levels is not permitted by convention. The cascade is monotonically restrictive as it descends.

The cascade answers two questions that come up in every serious Claude Code deployment. Where does context live when the operator works across multiple businesses or functions? In the cascade; not in one monolithic prompt. How does context evolve as the operator descends into specifics? Each level keeps its own scope honest; universal rules at the root, business specifics at the business level, function specifics at the function level.

The walker at `runtime/cascade_walker.py` resolves the chain for any directory. See [docs/cascade-pattern.md](docs/cascade-pattern.md) for the layer-by-layer treatment.

## 2. The hooks layer

The cascade is advisory. The model reads it, agrees with it, and intends to follow it. Under context pressure or prompt injection, the model can forget. The hooks layer is deterministic. Bash scripts fire on Claude Code lifecycle events and either pass or block, regardless of what the model intended.

Four hooks ship by default.

`pre-tool-use.sh` fires before every tool call. It blocks credential patterns, destructive bash commands, and external-action tools called without an explicit approval flag.

`post-tool-use.sh` fires after Write or Edit completes. It scans new file content for em dashes, banned vocabulary, throat-clearing phrases, and three-part list cadence. Code blocks and a documented exempt list are skipped.

`stop.sh` fires when the agent finishes a turn. It verifies the final message contains a session summary covering decided, built, changed, and next. Missing summaries block termination.

`pre-compact.sh` fires before Claude Code auto-compacts the session context window. It reads session state and emits a carry-forward block covering current task, current phase, active files, and non-negotiable constraints. The block becomes part of the post-compaction context.

The master principle: encode rules that must hold every time as hooks, keep judgment-dependent rules in CLAUDE.md. A rule only in CLAUDE.md will eventually be violated. A rule in a hook cannot be.

The hook simulator at `runtime/hook_simulator.py` runs any hook against a JSON fixture and reports the verdict. Lets an operator verify enforcement without a full session. See [docs/hooks-layer.md](docs/hooks-layer.md) for the design rationale.

## 3. The agent teams pattern

Most multi-agent systems share context promiscuously. Every agent sees every other agent's work. This is convenient and the source of the dominant production failure mode: groupthink at machine speed. Cortex-OS inverts the default. Each agent sees only what its role requires.

The pattern is hub-and-spoke. The orchestrator is the hub. Specialists are spokes. Five reference agents ship at `reference/agents/`: orchestrator, analyst, writer, researcher, reviewer. Two roles vary by domain (engineer and qa for software, domain-specialist and subject-matter-expert for other contexts).

Three boundary rules apply in every team.

The engineer never sees QA reports before implementation. An implementer that anticipates what QA will check optimizes for passing QA, not for correctness. QA arrives after implementation completes.

The data-scientist never sees UI decisions during analysis. Analysis shaped by an intended visualization smooths findings toward what charts well. Analysis runs to completion before the writer or designer sees output.

The QA never sees the implementation during development. QA that watched code get built tests the code as written rather than the requirements as specified. QA receives the completed artifact and the original requirements.

Three mechanisms enforce the boundaries together. Claude Code subagent invocation creates a fresh context for each agent. Agent frontmatter restricts tool access (the reviewer ships with `permissionMode: deny` and no Write/Edit access). The orchestrator's dispatch protocol passes the minimum input each role requires; prior agents' working context is not pasted in.

The reviewer's value is its blindness. A reviewer that sees the development context sympathizes with the choices. A reviewer that sees only the artifact judges it on its own terms. The pattern protects this property by design.

See [docs/agent-teams-pattern.md](docs/agent-teams-pattern.md) for the full treatment.

## 4. Schema discipline

Cortex-OS configurations are declarative. Three schemas govern the runtime decisions Claude Code makes.

Agent frontmatter (12 fields). Per-agent declaration of name, description, model, tools, disallowedTools, permissionMode, maxTurns, skills, mcpServers, hooks, memory, and background. Lives in the YAML block at the top of any agent definition file under `reference/agents/`.

`models.yaml`. Maps roles to specific Claude models with optional reasoning-effort hints. Agents reference roles; the runtime resolves the role to a concrete model at invocation time. Cascading: function-level models.yaml overrides business-level overrides root.

`tools.yaml`. Declares the project's tool inventory with per-tool failure protocols (retry, escalate, halt, log_and_continue). Each tool's protocol governs how the orchestrator handles errors from that tool.

The schema validator at `runtime/schema_validator.py` parses any of these files and reports violations. Validation runs on commit via the pressure-testing harness. Invalid schemas block the commit before the file reaches Claude Code's runtime, where invalid configurations would surface as silent failures.

See [docs/schema-reference.md](docs/schema-reference.md) for every field, type, allowed value, default, and example.

## 5. Skill auto-invocation

Claude Code skills are markdown files with YAML frontmatter that the runtime loads conditionally based on the user's prompt. A description matcher compares the prompt against each skill's description and triggers; high-relevance matches are pre-loaded into the session.

Cortex-OS treats skills as a fifth control layer. They are not part of the cascade (the cascade is for CLAUDE.md files) but they share the design property: the system decides what context loads, not the operator manually.

Three skill conventions matter in Cortex-OS.

Skills should be domain-narrow. A skill named `pressure-testing` should do one thing well. Skills that try to cover multiple unrelated concerns degrade auto-invocation precision.

Skill descriptions are the auto-invocation contract. The description should read like an instruction to another agent describing when to delegate to this skill. Imprecise descriptions cause false negatives or false positives.

Skills compose with agents. An agent's frontmatter can declare required skills via the `skills` field. Required skills load regardless of auto-invocation. The writer agent always loads `writing-style` and `voice-guide`; the auto-invocation matcher decides whether other skills also load.

The simulator at `runtime/skill_invocation_simulator.py` shows which skills would match for a given prompt and why. The matching algorithm in the simulator is a transparent approximation of Claude Code's internal logic.

## 6. The pressure-testing protocol

Pressure-testing is a quality gate that runs before any commit reaches the public branch. Seven checks operationalize the Hard Rules into automatable evaluations.

The seven:

AI signature scan. Em dashes in prose, banned vocabulary, throat-clearing phrases. The same checks the post-tool-use hook runs, applied at the diff level.

Veracity flag. Substantive numeric claims (currency, percentage, 3+ digits, decimals) appearing in paragraphs that lack a nearby citation marker.

Falsifiability flag. Soft hedges (could, possibly, perhaps, might) in sentences that lack a number or a conditional structure.

Confidence label check. For analytical content, every finding heading must carry a confidence label.

Scope drift heuristic. File length growth beyond a documented budget. Presence of sections not listed in the relevant spec.

Three-part cadence count. Counts the "X, Y, and Z" pattern. High counts flag for human review.

Sentence-length variance. Pure AI prose has low variance. Variance below a threshold flags for review.

The harness at `runtime/pressure_testing_harness.py` runs all seven against a file or directory. Findings are categorized as blocker (publication-stopping), major (must fix before publication), or minor (review but not blocking).

The protocol is not exhaustive. Judgment-dependent quality issues are still the operator's responsibility. The harness catches the deterministic violations and surfaces the rest for human review. This is the runtime counterpart to the architectural principle: hooks enforce, CLAUDE.md advises, the harness checks at commit time.

## Composition

The four layers and two cross-cutting concerns compose without ceremony. A working Cortex-OS session looks like this:

1. The operator opens Claude Code in a working directory.
2. Claude Code walks the cascade and loads every relevant CLAUDE.md.
3. The skill matcher loads required and auto-invoked skills.
4. The operator issues a prompt.
5. The model plans the work and calls tools.
6. Each tool call passes through `pre-tool-use.sh`.
7. Write and Edit outputs pass through `post-tool-use.sh`.
8. The orchestrator dispatches specialist agents under the context-boundary rules.
9. The session ends; `stop.sh` verifies the summary.
10. The operator commits; the pressure-testing harness gates the push.

Nothing in this loop requires a runtime beyond Claude Code itself. Cortex-OS is configuration, enforcement, and discipline on top of a runtime that already exists.
