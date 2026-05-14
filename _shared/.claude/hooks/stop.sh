#!/usr/bin/env bash
#
# stop.sh
# =======
# Fires when the agent finishes a turn or session. Verifies the
# session produced its required closing artifacts before allowing
# the loop to terminate.
#
# WHAT IT ENFORCES
#   1. Session summary present. The session must produce a
#      structured summary covering: decided, built, changed, next.
#      If the agent stops without producing one, the hook blocks
#      and asks for it.
#   2. Final-output AI signature scan. Re-runs the AI signature
#      checks against the final assistant message. This is a
#      catch-net for prose that was assembled across multiple
#      messages rather than committed via Write/Edit.
#
# WHY CLAUDE.MD CANNOT REPLACE THIS HOOK
#   The session summary is a state-persistence anchor. Without it,
#   the next session has no machine-readable handoff. The Session
#   Start Protocol in CLAUDE.md instructs the model to write one;
#   the hook ensures it actually did.
#
# TRIGGER
#   Claude Code invokes this hook when the agent stops generating.
#   The session transcript path is provided on stdin.
#
# INPUT (stdin, JSON)
#   {
#     "session_id": "...",
#     "transcript_path": "/path/to/session.jsonl" | null,
#     "stop_hook_active": true | false
#   }
#
# EXIT CODES
#   0  Session may stop.
#   2  Session must continue. Stderr instructs the model what is
#      missing. The model is given another turn.
#   1  Internal script error.
#

set -euo pipefail

PAYLOAD="$(cat)"

if ! command -v jq >/dev/null 2>&1; then
  echo "stop: jq not installed; cannot evaluate transcript." >&2
  exit 1
fi

ACTIVE="$(printf '%s' "$PAYLOAD" | jq -r '.stop_hook_active // false')"
if [ "$ACTIVE" = "true" ]; then
  exit 0
fi

TRANSCRIPT_PATH="$(printf '%s' "$PAYLOAD" | jq -r '.transcript_path // ""')"

if [ -z "$TRANSCRIPT_PATH" ] || [ ! -r "$TRANSCRIPT_PATH" ]; then
  exit 0
fi

LAST_ASSISTANT="$(tac "$TRANSCRIPT_PATH" \
  | grep -m1 '"role":"assistant"' \
  | jq -r '.message.content[0].text // ""' 2>/dev/null || true)"

if [ -z "$LAST_ASSISTANT" ]; then
  exit 0
fi

VIOLATIONS=()

# ---------- CHECK 1: SESSION SUMMARY PRESENT ----------
for anchor in 'decided' 'built' 'changed' 'next'; do
  if ! printf '%s' "$LAST_ASSISTANT" | grep -iq "$anchor"; then
    VIOLATIONS+=("session summary missing anchor: $anchor")
  fi
done

# ---------- CHECK 2: AI SIGNATURE SCAN ON FINAL OUTPUT ----------
if printf '%s' "$LAST_ASSISTANT" | grep -q '—'; then
  VIOLATIONS+=("final output contains em dash")
fi

BANNED_VOCAB='\b(delve|landscape|leverage|leverages|leveraging|robust|utilize|utilizes|utilizing|streamline|streamlines|spearhead|holistic|synergy|paradigm)\b'
if printf '%s' "$LAST_ASSISTANT" | grep -Eiq "$BANNED_VOCAB"; then
  HIT="$(printf '%s' "$LAST_ASSISTANT" | grep -Eio "$BANNED_VOCAB" | sort -u | tr '\n' ' ')"
  VIOLATIONS+=("final output contains banned vocabulary: $HIT")
fi

# ---------- REPORT ----------
if [ "${#VIOLATIONS[@]}" -gt 0 ]; then
  echo "stop: session cannot terminate cleanly. Issues:" >&2
  for v in "${VIOLATIONS[@]}"; do
    echo "  - $v" >&2
  done
  echo "Produce a session summary covering: Decided, Built, Changed, Next." >&2
  echo "Rewrite any AI-signature violations." >&2
  exit 2
fi

exit 0
