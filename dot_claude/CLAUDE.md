# Claude Code Configuration

## General Guidelines
- **You must think exclusively in English**. However, you are required to **respond in Japanese**.

## Python Exception Handling

- Never use bare `except:`, `except Exception:`, or `except BaseException:`. Always catch specific exception classes (e.g., `ValueError`, `FileNotFoundError`, `ConnectionError`, `KeyError`).
- If you must catch a broad range of exceptions (e.g., in a top-level handler), always log the exception and re-raise it with `raise`.
- Never silently swallow exceptions. Every `except` block must either handle the error meaningfully, log it, or re-raise it.

