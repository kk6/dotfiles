#!/bin/bash
# PostToolUse hook: remind to update README.md when key config files change
# Triggers on Edit and Write tools targeting CLAUDE.md, rules, hooks, skills, or settings

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // ""')

# Only check Edit and Write operations
if [[ "$tool_name" != "Edit" && "$tool_name" != "Write" ]]; then
  exit 0
fi

file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""')

# Check if the changed file is one that should trigger a README update reminder
should_remind=false
case "$file_path" in
  */CLAUDE.md)
    should_remind=true ;;
  */.claude/rules/*)
    should_remind=true ;;
  */.claude/hooks/*)
    should_remind=true ;;
  */.claude/skills/*)
    should_remind=true ;;
  */settings.json)
    should_remind=true ;;
esac

if [[ "$should_remind" == "true" ]]; then
  # Don't remind if README.md itself is being edited
  if [[ "$file_path" == */README.md ]]; then
    exit 0
  fi
  echo "README sync reminder: $file_path was modified. Check if README.md needs updating."
fi
