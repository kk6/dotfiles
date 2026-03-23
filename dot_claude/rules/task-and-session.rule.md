# Task & Session Standards

## Pre-Execution: Clarify Requirements

Before starting any non-trivial task:
- Identify what is being asked and what the acceptance criteria are.
- If the scope is ambiguous, ask a focused clarifying question — state what you already understand, then ask only what you don't.
- Do not proceed on assumptions when a quick question would prevent rework.

## Pre-Submission Checklist

Before delivering any output, verify:
- Does the output satisfy **every explicit requirement**?
- Is the scope appropriate — neither too narrow nor too wide?
- Does it conform to all active rules and project conventions?
- Is it internally consistent with no dead references?
- For code: does it compile/run? Are relevant tests passing?

## Proactive Status Communication

- After each major milestone, briefly state what was done and what comes next.
- If a blocker or unexpected finding arises, report it immediately.
- Format: "Completed [X]. Now working on [Y]. Remaining: [Z]."

## Early Escalation

If something unexpected occurs mid-task:
1. **Stop** — do not continue on assumptions.
2. **Report** — state what happened and its impact.
3. **Propose** — present options with trade-offs.

## Session Initialization

Before executing shell commands, read `~/.zshrc` to understand alias configuration (Rust-based tools, git pager, etc.).

## Progress Preservation

- Save progress by committing partial work with `WIP:` prefix or leaving a TODO comment.
- PR-related tasks (descriptions, review responses, refactoring) should be completed atomically.
