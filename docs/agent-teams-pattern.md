# Agent Teams Pattern

The agent teams pattern in Cortex-OS rests on one principle: **context boundaries are a control mechanism, not a limitation**.

Most multi-agent systems share context promiscuously. Every agent sees every other agent's work, every prior message, every intermediate decision. This is convenient. It is also the source of the dominant failure mode in production multi-agent systems: groupthink at machine speed. Agents that share context converge. Convergence inside a team is the most common origin of blind spots.

Cortex-OS inverts the default. By design, each agent sees only what its role requires. The pattern is closer to a well-run engineering organization than to a shared chat room.

## Why context boundaries matter

An adversarial reviewer that has watched the work get built will sympathize with the choices made along the way. A reviewer that sees only the final artifact judges it on its own terms. The first reviewer is comforting. The second is useful.

The same logic applies to every agent role. An analyst that has seen the intended downstream framing will narrow the analysis to support that framing. An analyst that sees only the question evaluates the evidence on its own terms. A researcher that has seen the desired conclusion will preferentially surface sources that support it.

Independence is not a default. It is something the system architecture must enforce.

## The seven-role pattern

A complete team for technical work has seven roles. Cortex-OS ships five reference implementations and leaves two for the operator to instantiate against their domain. The five reference agents at `reference/agents/` are:

`orchestrator` decomposes the objective, dispatches subtasks, and consolidates outputs. Sees the plan but not the internal drafting of teammates.

`analyst` interprets evidence and produces structured findings. Sees the question and the data sources but not the intended downstream framing.

`researcher` performs external research and produces citations. Sees the research question but not the desired conclusion.

`writer` drafts prose for human readers. Sees the structured input from upstream agents and the audience but not the reviewer's adversarial notes.

`reviewer` performs adversarial review of completed work. Sees the final artifact and the original objective. Sees nothing else.

The two roles that vary by domain are typically `engineer` and `qa` for software work, or `domain-specialist` and `subject-matter-expert` for other professional contexts. Both follow the same context-boundary rules as the reference five.

## The boundary rules

Every agent role in the pattern observes three rules.

**Rule 1: The engineer never sees QA reports before implementation.** An implementer that anticipates what QA will check optimizes for passing QA, not for correctness. The QA report arrives after the implementation is complete and is fed back through a fresh implementation cycle.

**Rule 2: The data-scientist never sees UI decisions during analysis.** A data analysis that has been shaped by the intended chart, table, or dashboard layout will smooth its findings toward what visualizes well. The analysis runs to completion before the writer or designer sees the output.

**Rule 3: The QA never sees the implementation during development.** QA that has watched the code get built will tend to test the implementation as written rather than the requirements as specified. QA receives the completed artifact and the original requirements; the implementation history stays inside the engineer's context.

These three rules generalize to every multi-agent team. The principle is the same: when a role's job is to judge or evaluate, deny it the development context that would bias the judgment.

## How the boundaries are enforced

Cortex-OS uses three mechanisms to enforce context boundaries.

First, each agent runs in an isolated subagent context. Claude Code's subagent invocation creates a fresh context for the subagent that does not inherit the parent's full transcript. The parent passes only the explicit input it chooses to pass.

Second, agent frontmatter restricts tool access. A reviewer with `permissionMode: deny` and no `Write` or `Edit` access cannot mutate the artifact under review; it can only report. A writer with no `WebSearch` access cannot wander into research that should have been done upstream.

Third, the orchestrator enforces boundary discipline as part of its dispatch protocol. When the orchestrator calls a teammate, it passes the minimum input the role requires. The reviewer receives the artifact and the objective. The analyst receives the question and the data. The orchestrator does not paste in the prior agents' working context.

## When the pattern breaks

The pattern fails when an operator routes around it. The most common failure: the operator chats directly with the reviewer, providing the context the reviewer was supposed to not see. At that point, the reviewer is no longer independent. The judgment is contaminated.

The protection against this failure is procedural, not technical. The operator must understand that the reviewer's value is its blindness. Adding context destroys the property the role was built for.

The same applies to every role with a context boundary. If the system is being used correctly, the orchestrator dispatches; teammates execute; the operator reads outputs. If the operator finds themselves arguing with a teammate mid-task, the team architecture has failed and the work should be restarted with a fresh dispatch.

## Reading the reference agents

Each reference agent at `reference/agents/` includes an explicit context-boundary section. The section names what the agent sees and what it does not see. The boundaries are not aspirational; the runtime enforces them via the frontmatter fields documented in `docs/schema-reference.md`.

Read the five reference agents in order: orchestrator, analyst, researcher, writer, reviewer. The progression mirrors the lifecycle of a typical work item: plan, gather, interpret, draft, review.
