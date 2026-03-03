# Task Completion Standards

## Pre-Execution: Clarify Requirements

Before starting any non-trivial task:
- Identify what is being asked and what the acceptance criteria are.
- If the scope is ambiguous, ask a focused clarifying question — state what you already understand, then ask only what you don't.
- Do not proceed on assumptions when a quick question would prevent rework.

## Pre-Submission Checklist

Before delivering any output (code, document, plan, or answer), verify each of the following:

### 1. Requirements Coverage
- Does the output satisfy **every explicit requirement** stated in the request?
- Are there items that were asked for but not addressed?
- Is the scope appropriate — neither too narrow (missing work) nor too wide (unsolicited changes)?

### 2. Constraints Compliance
- Does the output conform to all active rules (language, style, toolchain, framework conventions)?
- Does it follow the project's existing patterns and naming conventions?
- For Python: are exception handling rules, type hints, and linting standards respected?

### 3. Quality Gate
- Is the output internally consistent (no contradictions, no dead references)?
- For code: does it compile/run without errors? Are relevant tests passing?
- Would a reader unfamiliar with the immediate context understand it?

## Mid-Task Progress Reporting

For long-running or multi-step tasks, proactively surface status rather than going silent:
- After each major milestone, briefly state what was completed and what comes next.
- If a blocker or unexpected finding arises, report it immediately — do not wait until the end.
- A short mid-task update ("Completed X; now working on Y; blocked on Z") is always better than a late surprise.

## Early Escalation

If something unexpected occurs mid-task (scope is larger than estimated, requirements conflict, critical information is missing):
1. **Stop** — do not continue on assumptions.
2. **Report** — state clearly what was found.
3. **Propose** — present the decision needed and the options available.

Reporting a problem early gives the user time to act. Reporting it at the deadline leaves no room for recovery.
