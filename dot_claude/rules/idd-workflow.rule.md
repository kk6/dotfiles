# Intent-Driven Development (IDD) Workflow

## Core Principle

Development starts from **Intent**, not from specifications.
Intent consists of **Why** (motivation) and **What** (observable outcome) only.
**How** (implementation details) belongs in the code — never in Intent.

This extends the Coding Philosophy:

| Artifact              | Describes |
|-----------------------|-----------|
| Code                  | How       |
| Tests                 | What      |
| Commit messages       | Why       |
| Code comments         | Why not   |
| **Intent (ADR)**      | **Why + What (as a point-in-time decision record)** |

## Intent Document = ADR

Intent is recorded as an Architecture Decision Record (ADR).
ADRs are **immutable** — once accepted, they are never edited.
If a decision is overturned, create a new ADR that supersedes the old one.

This eliminates the sync problem: specifications claim to be "current truth" and drift from code,
but ADRs record "what was decided at that point in time" — drift is structurally impossible.

### What to include in Intent

- **Why** — Business motivation, user problem, technical constraint that drives the change
- **What** — Observable behavior, acceptance criteria, input/output contracts, success/failure conditions

### What to exclude from Intent

- Libraries, frameworks, or tools to use
- Internal data structures or algorithms
- Processing steps or execution order
- Any implementation detail that could change without affecting the Intent

## ADR Storage

- **Location**: `docs/adr/` in the project root
- **Naming**: `NNNN-<kebab-case-slug>.md` (e.g., `0001-introduce-user-authentication.md`)
- **Numbering**: Sequential, zero-padded to 4 digits. Never reuse numbers.

## ADR Template

```markdown
# ADR-NNNN: <Title>

## Status

proposed | accepted | superseded by [ADR-NNNN](NNNN-slug.md)

## Date

YYYY-MM-DD

## Context (Why)

Why is this change needed?
Describe the business motivation, user problem, or technical constraint.

## Intent (What)

What should be achieved?
Define observable behavior, acceptance criteria, and input/output contracts.
Do NOT describe how to implement it.

## Constraints

Non-functional requirements and boundaries (performance, security, compatibility).
These constrain the solution space without prescribing the implementation.

## Alternatives Considered

What options were evaluated and rejected? State the reason for each rejection.
(This is the "Why not" — valuable context for future decision-makers.)

## Consequences

What follows from this decision — both positive and negative trade-offs.
```

## ADR Lifecycle

1. **proposed** — Draft created, open for discussion
2. **accepted** — Decision finalized, implementation may begin
3. **superseded by ADR-NNNN** — A newer decision replaces this one

To reverse or modify a past decision:
- Do NOT edit the original ADR
- Create a new ADR with a link: "supersedes [ADR-NNNN](NNNN-slug.md)"
- Update the old ADR's status to: "superseded by [ADR-NNNN](NNNN-slug.md)"
  (This is the only permitted edit to an accepted ADR)

## When to Write an ADR

Write an ADR when:
- Introducing a new feature or capability
- Making an architectural or design decision with lasting impact
- Choosing between multiple viable approaches
- Changing or reversing a previous decision

Do NOT write an ADR for:
- Bug fixes (the commit message covers "why")
- Routine refactoring without design decisions
- Trivial changes where the intent is self-evident

## How-Leak Check

Before finalizing an Intent, verify it contains no How-leaks:

> "If I replaced every implementation detail with a different valid approach,
> would the Intent still accurately describe the goal?"

If yes — the Intent is clean. If no — extract the How-leaked parts.
