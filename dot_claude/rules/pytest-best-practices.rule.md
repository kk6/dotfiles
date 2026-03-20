# pytest Best Practices

## Test Method Naming

### Basic Format

```text
test_<subject>_<expected_behavior>_when_<precondition>
```

- `test_` prefix is required (needed for pytest test discovery)
- Use snake_case throughout
- The `when_` suffix may be omitted when the precondition is obvious

### Examples

```python
def test_extract_name_returns_name_when_present():
    ...

def test_extract_name_raises_value_error_when_missing():
    ...

def test_calculate_total_returns_zero_for_empty_cart():
    ...
```

### With Test Classes

- Name the class `Test<Subject>` and omit the subject from method names
- pytest output reads as `TestOrderProcessor::test_raises_error_when_customer_is_missing`

```python
class TestOrderProcessor:
    def test_raises_error_when_customer_is_missing(self):
        ...

    def test_creates_order_when_all_fields_valid(self):
        ...
```

### Naming Anti-patterns

- Meaningless names like `test_1`, `test_case_a`
- Including implementation details (e.g., mock usage) in the name
- Overly long names (keep under ~60 characters)
  - If too long, reconsider test granularity or move details to parametrize `ids`

### When Test Names Aren't Enough

If the scenario is too complex to express in ~60 characters, add a docstring to supplement the test name.
The docstring appears in pytest verbose output (`-v`) alongside the test name.

```python
def test_order_rejected_when_inventory_reserved():
    """Concurrent checkout: order placed after another user reserved
    the last item should be rejected, not silently succeed."""
    ...
```

- The test name stays concise for discovery and CI output
- The docstring explains **why** this case matters or **what** non-obvious scenario is being tested
- Do not add docstrings to self-explanatory tests — they become noise

## Arrange-Act-Assert (AAA) Pattern

Structure each test in three phases:

- **Arrange** — Set up the data and environment for the test
- **Act** — Execute the code under test
- **Assert** — Verify that the result matches expectations

```python
def test_add_numbers():
    # Arrange
    a = 5
    b = 7
    # Act
    result = a + b
    # Assert
    assert result == 12
```

- For longer tests, use comments to mark each phase for readability (short tests of a few lines do not need them)
- Keep Act to a single operation per test. Split into separate tests if multiple actions are needed

## Test Granularity and Independence

- One test = one behavior. Do not combine multiple behaviors in a single test
- Do not share state between tests. Each test must pass or fail on its own
- Tests must not depend on execution order

## Always Test Edge Cases

Go beyond standard inputs — explicitly cover:

- **Empty inputs**: empty string, empty list, `None`
- **Boundary values**: min/max, zero, negative numbers, single-element collections
- **Invalid inputs**: wrong types, out-of-range values

### Example: Testing Expected Exceptions

```python
import pytest

def test_division_raises_zero_division_error_when_divisor_is_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

## Using parametrize

- Keep function names general — describe the subject and behavior, not individual cases
- Delegate case descriptions to the `ids` parameter
- Never omit `ids` (ensures readable output on test failure)

```python
@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        ("hello", 5),
        ("", 0),
        ("  spaces  ", 10),
    ],
    ids=[
        "normal_string",
        "empty_string",
        "string_with_spaces",
    ],
)
def test_calculate_length(input_value, expected):
    assert calculate_length(input_value) == expected
```

## Test Isolation and Mocking

- Isolate external dependencies (APIs, databases, filesystem, clock) with mocks
- Keep mocking minimal — avoid tight coupling to implementation details
- Use `unittest.mock.patch` with the narrowest possible scope

```python
from unittest.mock import patch

def test_fetch_user_returns_user_when_api_succeeds():
    # Arrange
    mock_response = {"id": 1, "name": "Alice"}
    with patch("myapp.client.http_get", return_value=mock_response):
        # Act
        user = fetch_user(1)
    # Assert
    assert user.name == "Alice"
```

## Fixtures

- Extract shared setup into `@pytest.fixture`
- Prefer the smallest scope (default `function`)
- Place fixtures shared across multiple test files in `conftest.py`

```python
@pytest.fixture
def sample_order():
    return Order(item="Widget", quantity=3, price=9.99)

def test_order_total(sample_order):
    assert sample_order.total == pytest.approx(29.97)
```

## Test Coverage

- Do not aim for 100% coverage as a goal. Prioritize critical paths and complex logic
- Treat low-coverage areas as a **hint** for missing tests, not a target to fill
- Prioritize testing: branches, exception paths, and guard clauses
- Use `--cov` flag (via `pytest-cov`) to measure coverage and identify gaps
