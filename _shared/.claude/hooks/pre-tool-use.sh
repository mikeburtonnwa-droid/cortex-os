#!/usr/bin/env bash
#
# pre-tool-use.sh
# ===============
# Fires BEFORE any tool call executes. Deterministic gate on what
# Claude is about to do.
#
# WHAT IT ENFORCES
#   1. Sensitive data patterns. Blocks tool calls whose parameters
#      contain likely API keys, AWS keys, private keys, or paths to
#      .env files. Catches accidental commits of credentials before
#      the model writes them anywhere persistent.
#   2. Destructive bash commands. Blocks rm -rf on system paths,
#      fork bombs, dd to block devices, mkfs, format. The model
#      should not be able to wipe a disk because of a bad inference.
#   3. External-send without approval. Blocks tool calls that match
#      "send / post / publish / create_draft" patterns unless the
#      parameters carry an explicit approved=true sentinel.
#
# WHY CLAUDE.MD CANNOT REPLACE THIS HOOK
#   Constitutional rules in CLAUDE.md are advisory. The model reads
#   them, agrees, and intends to follow. Under context pressure or
#   prompt injection the model can forget. A hook cannot forget.
#   Hooks enforce; CLAUDE.md advises. The two layers are not
#   redundant; they are different layers of the same control system.
#
# TRIGGER
#   Claude Code invokes this script before every tool call. The
#   tool name and input parameters are delivered as a JSON object
#   on stdin.
#
# INPUT (stdin, JSON)
#   {
#     "tool_name": "Bash" | "Write" | "Edit" | <any tool>,
#     "tool_input": { ... tool-specific parameters ... },
#     "session_id": "..."
#   }
#
# EXIT CODES
#   0  Allow the tool call to proceed.
#   2  Block the tool call. Stderr is surfaced to the model so it
#      can correct course on the next turn.
#   1  Internal script error. Claude Code treats this as a block.
#

set -euo pipefail

PAYLOAD="$(cat)"

if ! command -v jq >/dev/null 2>&1; then
  echo "pre-tool-use: jq not installed; cannot evaluate tool call." >&2
  exit 1
fi

TOOL_NAME="$(printf '%s' "$PAYLOAD" | jq -r '.tool_name // ""')"
TOOL_INPUT_JSON="$(printf '%s' "$PAYLOAD" | jq -c '.tool_input // {}')"
INPUT_TEXT="$(printf '%s' "$TOOL_INPUT_JSON" | jq -r 'tostring')"

# ---------- CHECK 1: SENSITIVE DATA PATTERNS ----------
SENSITIVE_PATTERNS=(
  'AKIA[0-9A-Z]{16}'
  'aws_secret_access_key'
  '[A-Za-z0-9_\-]{40,}'
  'BEGIN [A-Z ]*PRIVATE KEY'
  '\.env(\.|$|[^a-zA-Z])'
  'DATABASE_URL='
  'STRIPE_(SECRET|API)_KEY'
  'OPENAI_API_KEY'
  'ANTHROPIC_API_KEY'
)

CONTEXT_KEYWORDS='(api[_-]?key|secret|token|password|credential|bearer)'

for pat in "${SENSITIVE_PATTERNS[@]}"; do
  if [ "$pat" = '[A-Za-z0-9_\-]{40,}' ]; then
    if printf '%s' "$INPUT_TEXT" | grep -Eqi "$CONTEXT_KEYWORDS" \
       && printf '%s' "$INPUT_TEXT" | grep -Eq "$pat"; then
      echo "pre-tool-use: blocked. Tool input contains a long opaque token near a credential keyword." >&2
      exit 2
    fi
    continue
  fi
  if printf '%s' "$INPUT_TEXT" | grep -Eqi "$pat"; then
    echo "pre-tool-use: blocked. Sensitive pattern matched: $pat" >&2
    exit 2
  fi
done

# ---------- CHECK 2: DESTRUCTIVE BASH ----------
if [ "$TOOL_NAME" = "Bash" ]; then
  CMD="$(printf '%s' "$TOOL_INPUT_JSON" | jq -r '.command // ""')"

  DESTRUCTIVE_PATTERNS=(
    'rm[[:space:]]+-rf?[[:space:]]+/($|[[:space:]])'
    'rm[[:space:]]+-rf?[[:space:]]+~($|[[:space:]])'
    'rm[[:space:]]+-rf?[[:space:]]+\*'
    ':\(\)\{[[:space:]]*:\|:&[[:space:]]*\}'
    'dd[[:space:]]+if=.*of=/dev/'
    'mkfs\.'
    'shutdown[[:space:]]+-'
    'init[[:space:]]+0'
    '>[[:space:]]*/dev/sd[a-z]'
  )

  for pat in "${DESTRUCTIVE_PATTERNS[@]}"; do
    if printf '%s' "$CMD" | grep -Eq "$pat"; then
      echo "pre-tool-use: blocked. Destructive bash pattern: $pat" >&2
      echo "Command was: $CMD" >&2
      exit 2
    fi
  done
fi

# ---------- CHECK 3: EXTERNAL SEND WITHOUT APPROVAL ----------
EXTERNAL_TOOL_PATTERNS='(_send|send_|_post|post_|publish|create_draft|send_email|send_message)'

if printf '%s' "$TOOL_NAME" | grep -Eqi "$EXTERNAL_TOOL_PATTERNS"; then
  APPROVED="$(printf '%s' "$TOOL_INPUT_JSON" | jq -r '.approved // false')"
  if [ "$APPROVED" != "true" ]; then
    echo "pre-tool-use: blocked. External-action tool $TOOL_NAME requires approved=true in parameters." >&2
    exit 2
  fi
fi

exit 0
