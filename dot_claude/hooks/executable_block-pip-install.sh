#!/bin/bash
# PreToolUse hook: block pip/pip3 install commands
# Receives tool input as JSON on stdin

cmd=$(jq -r '.tool_input.command // ""')

if echo "$cmd" | grep -qE '(^|;|&&|\|\|?)\s*(pip3?|python3?\s+-m\s+pip)\s+install'; then
  echo '{"decision":"block","reason":"pip install is prohibited on this system. Use uv add (for project deps) or uvx (for CLI tools) instead."}'
fi
