---
name: ai-review
description: Review a draft text (message, report, PR description, commit message, etc.) from the reader's perspective and suggest improvements.
---

## Instructions

The user will provide a draft text to review. If no text is provided as an argument, ask them to paste it.

Review the draft across the following dimensions and produce structured feedback:

### 1. Clarity
- Is there any sentence or phrase that a reader might misunderstand?
- Are there vague references (e.g., "the thing", "that issue", "as discussed") that lack sufficient context?
- Are sentences too long? Flag any that could be split.

### 2. Completeness
- Is any critical information missing (e.g., who, what, when, why, next steps)?
- Does the reader have everything they need to act on or understand this message?

### 3. Structure
- Does it lead with the most important point (conclusion or request first)?
- Is the logical flow easy to follow?
- Would bullet points or a table improve readability?

### 4. Tone
- Is the tone appropriate for the relationship and context (e.g., formal report vs. Slack message)?
- Could any phrasing come across as rude, dismissive, or unclear in intent?
- Are there softer alternatives for blunt or negative statements?

### 5. Action Items
- Are next steps, owners, and deadlines explicit?
- Is it clear what (if anything) the reader is expected to do?

## Output Format

Produce output in three sections:

**Summary** — One sentence describing the overall state of the draft (e.g., "Clear structure but missing a deadline and the opening buries the key request.").

**Issues** — A numbered list of specific problems found, each with:
- Location or quote from the draft
- What the problem is
- A concrete suggestion or rewrite

**Revised Draft** — A revised version of the full text incorporating all suggestions. Wrap it in a ```markdown``` block so the user can copy it cleanly.

## Notes
- Do not rewrite in a completely different voice — preserve the author's intent and style.
- If the draft is already strong, say so explicitly and keep the issue list short.
- Never fabricate facts; if context is needed to improve the draft, ask for it rather than guessing.
