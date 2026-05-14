#!/usr/bin/env bash
#
# post-tool-use.sh
# ================
# Fires AFTER a tool call completes successfully. Verifies the
# output meets writing standards before the model continues.
#
# WHAT IT ENFORCES
#   1. AI signature scan. After any Write or Edit, scan the new
#      file content for AI-signature patterns: em dashes mid-prose,
#      banned vocabulary (delve, leverage, robust, utilize,
#      streamline, holistic, synergy, paradigm, etc.), and
#      throat-clearing phrases ("it's important to note,"
#      "in conclusion").
#   2. Three-part list pattern detection. Flag prose containing
#      patterns like "X, Y, and Z" inside the same sentence when
#      none of X, Y, Z are list items. This is the AI cadence
#      that the AI Signature Prohibition rule targets.
#   3. Optional auto-format. If the tool was invoked by an engineer
#      agent and the file is code, run the appropriate formatter.
#
# WHY CLAUDE.MD CANNOT REPLACE THIS HOOK
#   The AI signature prohibition is a high-frequency violation.
#   The model writes prose. The model has trained on prose with
#   AI signatures. Instruction-following degrades across long
#   sessions. The hook fires on every Write/Edit and either passes
#   the output or returns it to the model with a specific
#   correction. Determinism, not aspiration.
#
# TRIGGER
#   Claude Code invokes this hook after a tool call completes,
#   passing tool name, tool input, and tool result on stdin.
#
# INPUT (stdin, JSON)
#   {
#     "tool_name": "Write" | "Edit" | <any tool>,
#     "tool_input": { ... },
#     "tool_response": { ... } | null,
#     "session_id": "..."
#   }
#
# EXIT CODES
#   0  Output passed all checks. Continue.
#   2  Output failed. Stderr explains the violation. Model gets
#      the feedback and is expected to rewrite.
#   1  Internal script error.
#

set -euo pipefail

PAYLOAD="$(cat)"

if ! command -v jq >/dev/null 2>&1; then
  echo "post-tool-use: jq not installed; cannot evaluate output." >&2
  exit 1
fi

TOOL_NAME="$(printf '%s' "$PAYLOAD" | jq -r '.tool_name // ""')"

case "$TOOL_NAME" in
  Write|Edit|NotebookEdit) : ;;
  *) exit 0 ;;
esac

FILE_PATH=""
NEW_CONTENT=""
case "$TOOL_NAME" in
  Write)
    FILE_PATH="$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.file_path // ""')"
    NEW_CONTENT="$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.content // ""')"
    ;;
  Edit|NotebookEdit)
    FILE_PATH="$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.file_path // ""')"
    NEW_CONTENT="$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.new_string // ""')"
    ;;
esac

case "$FILE_PATH" in
  *.md|*.markdown|*.txt|*.rst) : ;;
  *) exit 0 ;;
esac

# Exempt paths. Files that legitimately contain the banned tokens
# because they document the rule itself. The exemption matches on
# path suffix.
EXEMPT_SUFFIXES=(
  '_template/CLAUDE.md'
  '_shared/rules/ai-signature-prohibition.md'
  '_shared/rules/communication-style.md'
  'docs/hooks-layer.md'
  'docs/schema-reference.md'
)

for suffix in "${EXEMPT_SUFFIXES[@]}"; do
  case "$FILE_PATH" in
    *"$suffix") exit 0 ;;
  esac
done

VIOLATIONS=()

# ---------- CHECK 1: EM DASH IN PROSE ----------
# Allow em dash only inside fenced code blocks.
PROSE="$(printf '%s' "$NEW_CONTENT" | awk '
  BEGIN { in_code = 0 }
  /^```/ { in_code = !in_code; next }
  { if (!in_code) print }
')"

if printf '%s' "$PROSE" | grep -q '—'; then
  VIOLATIONS+=("em dash detected in prose (use commas, semicolons, periods, or en dashes)")
fi

# ---------- CHECK 2: BANNED VOCABULARY ----------
BANNED_VOCAB='\b(delve|landscape|leverage|leverages|leveraging|robust|utilize|utilizes|utilizing|streamline|streamlines|spearhead|holistic|synergy|paradigm)\b'

if printf '%s' "$PROSE" | grep -Eiq "$BANNED_VOCAB"; then
  HIT="$(printf '%s' "$PROSE" | grep -Eio "$BANNED_VOCAB" | sort -u | tr '\n' ' ')"
  VIOLATIONS+=("banned vocabulary: $HIT")
fi

# ---------- CHECK 3: THROAT-CLEARING PHRASES ----------
THROAT='(it'\''s important to note|it is important to note|it'\''s worth noting|it is worth noting|it bears mentioning|in conclusion|to summarize|in summary)'

if printf '%s' "$PROSE" | grep -Eiq "$THROAT"; then
  HIT="$(printf '%s' "$PROSE" | grep -Eio "$THROAT" | head -1)"
  VIOLATIONS+=("throat-clearing phrase: \"$HIT\"")
fi

# ---------- CHECK 4: THREE-PART LIST CADENCE ----------
THREE_PART_HITS="$(printf '%s' "$PROSE" \
  | grep -cE ', [a-zA-Z][a-zA-Z ]+, and [a-zA-Z]' || true)"

if [ "${THREE_PART_HITS:-0}" -gt 3 ]; then
  VIOLATIONS+=("$THREE_PART_HITS three-part list patterns detected (review for AI cadence)")
fi

# ---------- REPORT ----------
if [ "${#VIOLATIONS[@]}" -gt 0 ]; then
  echo "post-tool-use: AI signature violations in $FILE_PATH:" >&2
  for v in "${VIOLATIONS[@]}"; do
    echo "  - $v" >&2
  done
  echo "Rewrite the affected content. See _shared/rules/ai-signature-prohibition.md." >&2
  exit 2
fi

exit 0
