# Python Exception Handling — Detailed Guidelines

## Core Principle

Errors should be visible, not hidden. Silent failure is worse than a crash.
A crash with a traceback tells you exactly what went wrong and where.
A silently swallowed exception hides the root cause and creates hard-to-debug downstream failures.

## PROHIBITED Patterns

### 1. `pass` in except blocks (silent swallowing)

```python
# BAD — absolutely forbidden
except Exception:
    pass

# BAD — still silent swallowing even with specific exceptions
except (ProjectNotFoundError, APIError):
    pass

# BAD — catching broad exception and continuing with fallback
except Exception:
    result = None  # hides the real error
```

### 2. Wrapping large blocks in try-except

```python
# BAD — too much code in try block, unclear what error is expected
try:
    data = load_config()
    processed = transform(data)
    result = api_call(processed)
    save_result(result)
except Exception as e:
    print(f"Error: {e}")
    return None
```

### 3. "Defensive" try-except that hides bugs

```python
# BAD — if project fetch fails, that's a bug worth knowing about
try:
    title = fetch_project_title(slug)
except Exception:
    title = slug  # silently masks API errors, auth issues, network problems
```

## CORRECT Patterns

### 1. Catch only specific, expected exceptions at system boundaries

```python
# GOOD — specific exception, clear recovery action
try:
    with open(config_path) as f:
        data = f.read()
except FileNotFoundError:
    logger.warning("Config not found at %s, using defaults", config_path)
    data = DEFAULT_CONFIG
```

### 2. Let unexpected errors propagate

```python
# GOOD — no try-except needed for internal logic
result = complex_processing(data)  # if this fails, we WANT to see the traceback
```

### 3. When you must handle errors, log and/or re-raise

```python
# GOOD — log context, then re-raise
try:
    response = await client.get(url)
except httpx.ConnectError:
    logger.error("Failed to connect to %s", url)
    raise
```

### 4. Top-level entry points may catch broadly, but must log and re-raise

```python
# GOOD — only at the very top level (e.g., main())
try:
    app.run()
except KeyboardInterrupt:
    sys.exit(0)
except Exception:
    logger.exception("Unhandled error")  # logs full traceback
    raise
```

## Decision Checklist

Before writing a try-except block, ask:

1. **What specific exception do I expect here?** → If you can't name it, don't catch it.
2. **Is this a system boundary?** (file I/O, network, user input) → If not, probably don't need try-except.
3. **What will I do in the except block?** → If the answer is "nothing" or "return None", remove the try-except entirely.
4. **Will this hide bugs during development?** → If yes, remove it. Debuggability > "safety".
