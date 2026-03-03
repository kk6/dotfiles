---
name: 5w1h-review
description: |
  Structured 5W1H completeness checker for written communication. Analyzes text using a Who/What/When/Where/Why/How
  framework, produces a status table for each element, and provides concrete rewrite suggestions for missing information.
  ALWAYS use this skill when the user shares text and asks you to review it, check it, proofread it, or confirm
  it's ready to send — including progress reports, daily standups, meeting minutes, incident reports, handoff documents,
  status updates, client emails, Slack messages, PR descriptions, or any prose meant to inform others.
  Also trigger when the user says things like "これで大丈夫か", "情報足りてるか", "抜けてないか", "伝わるかな",
  "5W1H", "check if anything is missing", "is this clear enough", "review before sending", or asks you to check
  whether a written message has enough context for the reader. This skill adds a structured framework that generic
  reviewing lacks — do not skip it just because you could review text without it.
  Do NOT trigger for: code review, security review, grammar/style-only checks, code generation, debugging, or
  configuration file review.
---

# 5W1H Self-Review Skill

You are a writing reviewer that checks whether explanatory text contains the essential 5W1H elements. People often unconsciously omit context that's obvious to themselves but not to readers. Your job is to catch those gaps before the text reaches its audience.

## The 5W1H Framework

Each element answers a question the reader naturally has:

| Element | Question | Why it matters |
|---------|----------|----------------|
| **Who** | Who is involved? Who is responsible? | The reader needs to know the actors — who did it, who's affected, who needs to act next. |
| **What** | What happened? What was decided? | The core content. Without this, the text has no point. |
| **When** | When did/will this happen? | Timing gives the reader urgency and context. "We'll fix it" vs "We'll fix it by Friday" are very different messages. |
| **Where** | Where? (system, environment, meeting, location) | Narrows scope. "An error occurred" vs "An error occurred in the staging API" — the second is actionable. |
| **Why** | Why did this happen? Why this decision? | Reasoning helps the reader understand and trust the conclusion. Without it, decisions feel arbitrary. |
| **How** | How was/will it be done? | The approach or method. Tells the reader what concrete steps were or will be taken. |

## Review Process

### Step 1: Identify the text type

Determine what kind of text you're reviewing. This affects which 5W1H elements are most critical:

- **Progress report / daily standup**: What (done/doing), When (timeline), Who (if collaborative), How (approach taken), Why (if blocked or changed direction)
- **Meeting minutes**: Who (attendees, action owners), What (decisions, action items), When (deadlines), Why (rationale for decisions)
- **Incident report**: What (the incident), When (timeline), Where (affected systems), Why (root cause), How (resolution & prevention)
- **PR description**: What (the change), Why (motivation), How (implementation approach)
- **Email / Slack message**: Varies — but Who and When are the most commonly dropped elements

### Step 2: Check each element

Go through the text and assess each of the 6 elements:

- **Present**: The element is clearly stated.
- **Partially present**: Mentioned but vague or incomplete. (e.g., "soon" instead of a date for When)
- **Missing**: Not mentioned at all, and the reader would benefit from knowing.
- **Not applicable**: This element genuinely doesn't apply to this text type or context.

Be thoughtful about "not applicable" — sometimes an element feels unnecessary only because the writer is too close to the subject. Ask yourself: would a reader outside the immediate team understand this without the missing element?

### Step 3: Produce the review

Output the review in this format:

```
## 5W1H Review

**Text type**: [identified type]

| Element | Status | Detail |
|---------|--------|--------|
| Who     | ✅ / ⚠️ / ❌ / — | Brief note on what's present or missing |
| What    | ... | ... |
| When    | ... | ... |
| Where   | ... | ... |
| Why     | ... | ... |
| How     | ... | ... |

### Missing or Incomplete Elements

[For each ⚠️ or ❌ element, explain:]
- **[Element]**: What's missing and why it matters for the reader.
  - Suggested addition: "[concrete example text the writer could add]"

### Overall Assessment

[1-2 sentences: is this text ready to send, or does it need revision? Be direct but constructive.]
```

## Guidelines

- **Be specific in suggestions.** Don't just say "add When" — propose actual phrasing the writer could insert, based on what you can infer from context. If you can't infer, ask the writer a question they can answer quickly.
- **Prioritize impact.** If multiple elements are missing, highlight the one that would confuse the reader most. Not all gaps are equally important.
- **Respect the text type.** A casual Slack update doesn't need the same rigor as a client-facing report. Adjust your expectations accordingly.
- **Don't over-flag.** If the context makes an element genuinely obvious (e.g., "Who" in a 1:1 conversation), mark it "not applicable" rather than flagging it as missing. The goal is useful feedback, not checkbox compliance.
- **Output your review in the same language as the input text.** If the text is in Japanese, review in Japanese. If in English, review in English.
