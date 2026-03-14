# Claude Code Configuration

## General Guidelines

- **You must think exclusively in English**. However, you are required to **respond in Japanese**.
- Disable installation of external libraries via pip for macOS's Python and homebrew's Python.
  - if you want to use external tools like ruff, consider using them via uvx.

## Coding Philosophy

- **Code** describes **How** — implementation details belong in the code itself.
- **Test code** describes **What** — what behavior is expected and being verified.
- **Commit messages** describe **Why** — the reason the change was made.
- **Code comments** describe **Why not** — why alternatives were rejected or avoided.

## Response Structure

- **Lead with the conclusion** (BLUF: Bottom Line Up Front). State the direct answer or result first, then provide reasoning, details, or caveats.
- Use bullet points over prose for lists of steps, options, or items.
- Do not omit context the reader needs to understand the response; do not include context they clearly already have.
- See `rules/task-completion.rule.md` for pre-submission verification standards.
