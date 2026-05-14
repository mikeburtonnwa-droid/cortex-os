#!/usr/bin/env bash
#
# pre-compact.sh
# ==============
# Fires BEFORE Claude Code auto-compacts the session context window.
# Re-injects the critical state that would otherwise be lost when
# older messages are summarized away.
#
# WHAT IT INJECTS
#   1. Current task. The single thing the session is presently
#      working on. Read from .claude/session-state.json if present;
#      otherwise omitted.
#   2. Active files. The set of file paths the session has touched
#      most recently. Read from the same state file.
#   3. Key constraints. A short list of constraints the model must
#      carry across the compaction boundary: identity, hard rules
#      reminder, current phase of work.
#
# WHY CLAUDE.MD CANNOT REPLACE THIS HOOK
#   Context compaction is a destructive operation on the model's
#   working memory. The model can be instructed to "remember the
#   current task" but cannot itself prevent earlier messages from
#   being summarized away. The hook fires BEFORE compaction and
#   injects content that survives into the new context. State
#   persistence is a property of the system, not the model.
#
# TRIGGER
#   Claude Code invokes this hook before auto-compaction. The
#   session id and transcript path are provided on stdin. The
#   hook's stdout is injected into the new context.
#
# INPUT (stdin, JSON)
#   {
#     "session_id": "...",
#     "transcript_path": "/path/to/session.jsonl",
#     "trigger": "auto" | "manual"
#   }
#
# OUTPUT (stdout)
#   Plain text. Becomes part of the post-compaction context.
#
# EXIT CODES
#   0  Injection successful (or nothing to inject).
#   1  Internal script error. Compaction proceeds without injection.
#

set -euo pipefail

PAYLOAD="$(cat)"

if ! command -v jq >/dev/null 2>&1; then
  exit 1
fi

STATE_FILE=""
for candidate in \
    ".claude/session-state.json" \
    "$HOME/.claude/session-state.json"; do
  if [ -r "$candidate" ]; then
    STATE_FILE="$candidate"
    break
  fi
done

CURRENT_TASK=""
ACTIVE_FILES=""
CURRENT_PHASE=""

if [ -n "$STATE_FILE" ]; then
  CURRENT_TASK="$(jq -r '.current_task // ""' "$STATE_FILE")"
  ACTIVE_FILES="$(jq -r '.active_files[]? // empty' "$STATE_FILE" | head -10)"
  CURRENT_PHASE="$(jq -r '.current_phase // ""' "$STATE_FILE")"
fi

cat <<EOF
[PRE-COMPACT CARRY-FORWARD]

Context was just compacted. The following state must be preserved
across the compaction boundary.

CURRENT TASK:
${CURRENT_TASK:-(no current task recorded)}

CURRENT PHASE:
${CURRENT_PHASE:-(no phase recorded)}

ACTIVE FILES (most recent):
${ACTIVE_FILES:-(no active files recorded)}

NON-NEGOTIABLE CONSTRAINTS:
- Hard Rules in the root CLAUDE.md still apply.
- AI Signature Prohibition still applies.
- Scope discipline: do not expand beyond what was explicitly requested.
- Veracity: no hallucinated facts, citations, or data.

If any of the above is missing or stale, ask the operator to
restate the current task before continuing.
EOF

exit 0
