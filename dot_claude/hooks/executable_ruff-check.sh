#!/usr/bin/env bash
# Stop hook: run ruff on Python files changed during the session.
# Only runs if ruff is available and there are staged/unstaged .py changes.

command -v ruff >/dev/null 2>&1 || exit 0

# Collect changed Python files (staged + unstaged + untracked)
changed_files=$(git diff --name-only --diff-filter=ACMR HEAD 2>/dev/null | grep '\.py$')
untracked_files=$(git ls-files --others --exclude-standard 2>/dev/null | grep '\.py$')
files=$(echo -e "${changed_files}\n${untracked_files}" | sort -u | grep -v '^$')

[ -z "$files" ] && exit 0

# Filter to files that actually exist
existing_files=""
for f in $files; do
  [ -f "$f" ] && existing_files="$existing_files $f"
done
[ -z "$existing_files" ] && exit 0

errors=""

# Lint check
lint_output=$(ruff check $existing_files 2>&1)
if [ $? -ne 0 ]; then
  errors="$errors\n--- ruff check ---\n$lint_output"
fi

# Format check
fmt_output=$(ruff format --check $existing_files 2>&1)
if [ $? -ne 0 ]; then
  errors="$errors\n--- ruff format --check ---\n$fmt_output"
fi

if [ -n "$errors" ]; then
  echo -e "$errors"
  exit 1
fi
