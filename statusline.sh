#!/bin/bash

# Claude Code statusline script
# Displays: directory name, model, git branch, python version, context usage

input=$(cat)

# Extract current working directory and get directory name
cwd=$(echo "$input" | jq -r '.workspace.current_dir')
dir_name=$(basename "$cwd")

# Extract and format model name
model_name=$(echo "$input" | jq -r '.model.display_name')
if [[ "$model_name" =~ ([A-Za-z]+[[:space:]][0-9.]+) ]]; then
    short_model="${BASH_REMATCH[1]}"
else
    short_model="$model_name"
fi
model_display=" $(printf '\033[32m')[$short_model]$(printf '\033[0m')"

# Git branch information
git_branch=""
if git -C "$cwd" rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git -C "$cwd" -c core.useReplaceRefs=false branch --show-current 2>/dev/null || \
             git -C "$cwd" -c core.useReplaceRefs=false rev-parse --short HEAD 2>/dev/null)

    if [ -n "$branch" ]; then
        if ! git -C "$cwd" -c core.useReplaceRefs=false diff --quiet 2>/dev/null || \
           ! git -C "$cwd" -c core.useReplaceRefs=false diff --cached --quiet 2>/dev/null; then
            git_status="*"
        else
            git_status=""
        fi
        git_branch=" on $(printf '\033[35m')$branch$git_status$(printf '\033[0m')"
    fi
fi

# Python version information
python_version=""
if [ -f "$cwd/pyproject.toml" ] || [ -f "$cwd/setup.py" ] || [ -f "$cwd/requirements.txt" ]; then
    if command -v python3 &> /dev/null; then
        py_ver=$(python3 --version 2>&1 | cut -d' ' -f2)
        python_version=" via $(printf '\033[33m')🐍 v$py_ver$(printf '\033[0m')"
    fi
fi

# Context window usage percentage
context_pct=""
usage=$(echo "$input" | jq '.context_window.current_usage')
if [ "$usage" != "null" ]; then
    current=$(echo "$usage" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
    size=$(echo "$input" | jq '.context_window.context_window_size')
    pct=$((current * 100 / size))
    context_pct=" [$(printf '\033[36m')${pct}%$(printf '\033[0m')]"
fi

# Output formatted statusline
printf "$(printf '\033[36m')%s$(printf '\033[0m')%s%s%s%s" \
    "$dir_name" "$model_display" "$git_branch" "$python_version" "$context_pct"
