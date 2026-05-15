---
name: context-management
description: Manage long-running plans across context compactions, session boundaries, and multi-day workflows. Use for orchestrator agents coordinating work that spans more than a single session. Pairs with the pre-compact hook for state survival.
triggers:
  - long-running task
  - multi-session work
  - state persistence
  - context compaction
  - session handoff
  - resume work
---

# Context Management

Long-running work outlives any single Claude Code session. Context windows fill. Sessions end. Compactions destructively summarize older messages. State persistence is a property of the system, not the model.

## The state file

Cortex-OS uses a session state file at `.claude/session-state.json` as the durable record of what a session has been doing. The pre-compact hook reads this file and injects its content into the post-compaction context.

The state file's canonical shape:

```json
{
  "current_task": "string - one sentence describing the active work",
  "current_phase": "string - which phase of a multi-phase plan",
  "active_files": ["array of file paths the session has touched"],
  "open_questions": ["array of strings - questions the operator must answer"],
  "last_updated": "ISO-8601 timestamp"
}
```

The orchestrator updates this file at every significant transition: when a new subtask begins, when a phase completes, when an open question is resolved, when the session prepares to pause.

## What to carry forward

Three categories of state must survive a session boundary.

The current task. A one-sentence description of what the session is presently working on. Specific enough that a new session can pick up without needing the operator to re-explain.

The active files. The set of files the session has recently touched. Lets the next session re-orient quickly to what is in flight.

Open questions. Anything the operator has not yet answered. Without this, the next session does not know what is blocking.

## What not to carry forward

Three categories of state should never reach the next session.

Internal reasoning chains. The session's intermediate thinking. The next session forms its own reasoning; importing prior reasoning creates anchoring effects that destroy independence.

Failed attempts. What the previous session tried and rejected. Documenting failures publicly is useful; carrying them forward as silent context is not.

Drafts under iteration. A draft of a deliverable in progress should live in the file system, not in carry-forward state. The next session opens the file fresh.

## After a compaction

When the pre-compact hook fires, the carry-forward block becomes part of the post-compaction context. The first thing the model should do on a new context is re-orient against the carry-forward.

The orientation pattern:

1. Read the carry-forward block from the injected context.
2. Read the current state file from disk to confirm it matches.
3. Read the active files listed in state.
4. Restate the current task in one sentence before continuing.

If the carry-forward and the state file disagree, the state file wins. The hook injects what was in the file at compaction time; the file may have been updated since.

## Session start protocol

The session start protocol in the root CLAUDE.md instructs the model to read MASTER_PLAN.md, identify the current phase, confirm the cascade has loaded, and state the working context in one sentence.

If MASTER_PLAN.md and the state file disagree, MASTER_PLAN.md is the operator's intent and wins on the multi-day picture. The state file is the in-flight detail and wins on the within-session picture.

## Session end protocol

Before stopping, the model produces a session summary with four anchors: decided, built, changed, next. The stop hook verifies the summary is present.

The summary is also the input for updating the state file. Use `runtime/current_reality_updater.py` to rewrite the Current Reality block in the relevant CLAUDE.md with the session's outcomes. The next session reads the updated reality from the cascade.

## Asking the operator

In three cases, the model should ask the operator before continuing rather than guess from state.

First: the state file is missing or empty after what should have been a multi-session workflow. The previous session ended without updating state; the operator must restate context.

Second: the carry-forward conflicts with the state file in a way that suggests an interrupted update. The operator must clarify which version is correct.

Third: a substantive change has happened externally (the operator manually edited a file, an external tool wrote new state, a different agent worked on the same project) that the carry-forward does not reflect. The operator must reconcile.
