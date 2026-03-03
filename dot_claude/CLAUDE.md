# Claude Code Configuration

## General Guidelines

- **You must think exclusively in English**. However, you are required to **respond in Japanese**.

## Response Structure

- **Lead with the conclusion** (BLUF: Bottom Line Up Front). State the direct answer or result first, then provide reasoning, details, or caveats.
- Use bullet points over prose for lists of steps, options, or items.
- Do not omit context the reader needs to understand the response; do not include context they clearly already have.
- See `rules/task-completion.rule.md` for pre-submission verification standards.

## Python Exception Handling (STRICT — violations are unacceptable)

- **`pass` in `except` blocks is FORBIDDEN.** Never write `except ...: pass`. There are NO exceptions to this rule.
- **Never use `except Exception:` or `except BaseException:`.** Always catch the most specific exception class possible.
- **Do NOT over-apply `try-except`.** Most code should NOT be wrapped in try-except. Only add error handling where a specific, recoverable error is expected at a system boundary (file I/O, network, user input).
- **Let unexpected errors propagate.** If you don't know exactly what error to expect, don't catch anything — let it crash with a full traceback.
- If you must catch a broad range of exceptions (e.g., in a top-level entry point), always log the full exception and re-raise it.
- See `rules/python-exception-handling.rule.md` for detailed examples of prohibited and correct patterns.
