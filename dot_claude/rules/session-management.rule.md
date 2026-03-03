# Session Management

## Initialization
**Required Action**: Before providing any command-line suggestions or executing shell commands, read `~/.zshrc` to understand the current alias configuration. Pay special attention to:
- Rust-based tool aliases (`lsd`, `fd`, `bat`, etc.)
- Git pager settings
- Any custom command configurations

## Progress Preservation

When sessions end mid-implementation, always save progress by committing partial work with 'WIP:' prefix or leaving a TODO comment summarizing next steps.

## Task Completion

For PR-related tasks, always complete the full generation/implementation before pausing - PR descriptions, review responses, and refactoring should be atomic operations.

## Proactive Status Communication

Do not wait to be asked "how is it going?" — report status proactively:

- After completing each major step in a multi-step task, briefly state what was done and what comes next.
- If a task is taking longer than a single response, surface an intermediate update rather than staying silent.
- Format: "Completed [X]. Now working on [Y]. Remaining: [Z]."

## Problem Escalation

When an unexpected issue arises mid-task, escalate immediately using this structure:

1. **What happened** — describe the finding or blocker objectively.
2. **What it means** — explain the impact on the current task.
3. **Options** — present two or more paths forward, with trade-offs if relevant.

Never: silently work around a problem, make an undisclosed assumption, or defer a known blocker to the end of the task.
