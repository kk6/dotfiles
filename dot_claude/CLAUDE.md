# Claude Code Configuration

## Session Initialization

**Required Action**: Before providing any command-line suggestions or executing shell commands, read `~/.zshrc` to understand the current alias configuration. Pay special attention to:

- Rust-based tool aliases (`lsd`, `fd`, `bat`, etc.)
- Git pager settings
- Any custom command configurations

This ensures all command suggestions align with the actual shell environment.

## Development Workflow Preferences

### Project Structure
- Uses **uv** for Python package management
- Prefers **Docker** for development environments
- **AWS** for production/staging environments
- **pytest** for testing with AAA pattern (Arrange-Act-Assert)

### Code Style
- **Python**: PEP 8 compliant, type hints preferred
- **Line length**: 88 characters (Black/Ruff standard)
- **Import order**: Standard lib, third-party, local modules
- **Docstrings**: Google style preferred
- **Logging**: Never use f-strings in logging statements

### Git Workflow
- Uses conventional commits
- Prefers feature branches
- Code review through PRs
- Uses semantic versioning

## Python Testing Best Practices ⚠️

### Module Caching Issues
Python's module caching can cause test isolation problems, especially when:
- Tests patch environment variables with `patch.dict()`
- Modules initialize objects at module level
- Multiple tests import the same modules

**Problem**: Cached modules retain old environment/state, causing test failures or false positives.

**Solution**: Clear module cache before importing in tests:
```python
def test_with_environment_patch():
    with patch.dict(os.environ, {"VAR": "new_value"}):
        # Clear relevant modules from cache
        sys.modules.pop("myproject.module", None)
        sys.modules.pop("myproject.config", None)

        from myproject import module  # noqa: E402
        # Now fresh import with new environment
```

**For multiple related modules**:
```python
# Clear all project modules
modules_to_clear = [name for name in sys.modules.keys() if name.startswith("myproject")]
for module in modules_to_clear:
    sys.modules.pop(module, None)
```

### Exception Testing Issues
`pytest.raises` may fail to catch custom exceptions due to:
- Module caching causing class identity mismatches
- Exception inheritance hierarchies
- Exception transformation layers

**Solution**: Use explicit try/except with isinstance checks:
```python
# Instead of this (may fail)
with pytest.raises(CustomError):
    some_function()

# Use this (more reliable)
try:
    some_function()
    assert False, "Expected exception but none was raised"
except Exception as e:
    from myproject.exceptions import CustomError
    assert isinstance(e, (BuiltinError, CustomError)), f"Unexpected: {type(e)}"
```

### Testing Fixtures with Environment
```python
@pytest.fixture
def clean_environment():
    """Fixture that ensures clean module imports with patched environment."""
    with patch.dict(os.environ, {"KEY": "test_value"}):
        # Clear project modules
        project_modules = [name for name in sys.modules.keys() if name.startswith("myproject")]
        for module in project_modules:
            sys.modules.pop(module, None)

        yield  # Test runs here with clean environment

        # Cleanup is automatic when fixture ends
```

### Common Python Testing Gotchas
1. **Import order in tests**: Import project modules AFTER environment setup to ensure proper configuration loading
2. **Mutable default arguments**: Avoid `def func(items=[]):` - use `def func(items=None): items = items or []`
3. **Global state pollution**: Always reset global variables/singletons between tests
4. **Async testing**: Use `pytest-asyncio` and proper event loop isolation
5. **Temp file cleanup**: Use `tempfile.TemporaryDirectory()` context manager for automatic cleanup

### When to Use Module Cache Clearing
- ✅ Tests that patch `os.environ`
- ✅ Tests that mock module-level constants/singletons
- ✅ Integration tests importing entire applications
- ✅ Tests running with different configuration files
- ❌ Simple unit tests with isolated functions
- ❌ Tests that don't change global state

## Tips for Effective Collaboration
- Always check for aliases before using standard commands
- Prefer modern Rust-based tools when available
- Use type hints and proper docstrings in Python code
- Follow the document-first approach for the Minerva project
- Test thoroughly with pytest using AAA pattern
- **Watch for module caching issues in tests** - clear `sys.modules` when patching environment

## Testing Strategy

### Core Testing Principles
- **Test isolation**: Each test should be independent and not rely on other tests
- **Single responsibility**: One test should test one behavior
- **Clear test names**: Use descriptive names that explain what is being tested
- **AAA pattern**: Follow Arrange-Act-Assert with clear section comments
- **Test coverage target**: Maintain 92%+ code coverage
- **Mock external dependencies**: File system, environment variables, API calls

### Test Organization Best Practices

#### Project Structure
```
tests/
├── unit/              # Fast, isolated tests for individual functions
│   ├── models/
│   ├── services/
│   └── utils/
├── integration/       # Tests for component interactions
│   ├── test_api_endpoints.py
│   └── test_service_integration.py
├── e2e/              # End-to-end workflow tests
│   └── test_full_workflows.py
├── fixtures/         # Shared fixtures (optional)
│   ├── fixtures_db.py
│   └── fixtures_mock.py
├── conftest.py       # Shared fixtures and pytest configuration
└── pytest.ini        # Pytest configuration
```

#### Test Discovery Configuration
In `pyproject.toml`:
```toml
[tool.pytest.ini_options]
addopts = [
    \"--import-mode=importlib\",  # Recommended for new projects
    \"--strict-markers\",         # Enforce marker registration
]
testpaths = [\"tests\"]
python_files = [\"test_*.py\", \"*_test.py\"]
python_classes = [\"Test*\"]
python_functions = [\"test_*\"]
```

### Fixture Management

#### Fixture Scopes and When to Use Them
- **function** (default): New instance for each test function
- **class**: Shared across all methods in a test class
- **module**: Shared across all tests in a module
- **session**: Shared across the entire test session

#### Fixture Best Practices
```python
# Use yield fixtures for setup/teardown
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

# Factory fixtures for multiple instances
@pytest.fixture
def make_user():
    def _make_user(name, age=None):
        return User(name=name, age=age or 25)
    return _make_user

# Fixture composition
@pytest.fixture
def authenticated_client(client, user):
    client.login(user)
    return client
```

#### conftest.py Organization
- Place common fixtures in `tests/conftest.py`
- Use local `conftest.py` files for directory-specific fixtures
- Consider a hybrid approach for large projects:
  - Global fixtures in root `conftest.py`
  - Specialized fixtures in `fixtures/` directory
  - Local fixtures in subdirectory `conftest.py` files

### Parametrization Best Practices

```python
# Basic parametrization
@pytest.mark.parametrize(\"input,expected\", [
    (\"\", True),
    (\"a\", True),
    (\"Bob\", True),
    (\"Never odd or even\", True),
    (\"abc\", False),
])
def test_is_palindrome(input, expected):
    assert is_palindrome(input) == expected

# Multiple parameters with IDs
@pytest.mark.parametrize(
    \"a,b,expected\",
    [
        (2, 3, 5),
        (-10, 5, -5),
        (0, 0, 0),
    ],
    ids=[\"positive\", \"negative\", \"zero\"]
)
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Markers and Test Categories

```python
# Register markers in pytest.ini
[pytest]
markers =
    slow: marks tests as slow
    unit: unit tests
    integration: integration tests
    e2e: end-to-end tests
    db: tests requiring database

# Use markers in tests
@pytest.mark.slow
@pytest.mark.integration
def test_complex_workflow():
    pass

# Run specific markers
# pytest -m \"unit and not slow\"
# pytest -m integration
```

### Property-Based Testing with Hypothesis
Minerva uses property-based testing to discover edge cases automatically:

- **Target areas**: Path validation, filename validation, tag operations, search functionality
- **Test files**: `tests/*_properties.py` (separate from traditional unit tests)
- **Performance**: ~5-6x slower than unit tests but provides much broader input coverage
- **Edge cases discovered**: Unicode handling, regex escaping, validation order dependencies
- **Documentation**: See `docs/property_based_testing.md` for comprehensive guidelines

**Commands**:
- Run property-based tests: `uv run pytest tests/*_properties.py`
- Reduce examples for CI: `uv run pytest --hypothesis-max-examples=20`
- Debug with seed: `uv run pytest --hypothesis-seed=12345`

### Testing Gotchas and Solutions ⚠️

#### Module Caching Issues
Python's module caching can cause test isolation problems when patching environment variables:

```python
# Problem: Cached modules retain old environment
def test_with_env_patch():
    with patch.dict(os.environ, {\"VAR\": \"new_value\"}):
        # If module was already imported, it uses old env
        from myproject import module  # May fail!

# Solution: Clear module cache before importing
def test_with_env_patch():
    with patch.dict(os.environ, {\"VAR\": \"new_value\"}):
        # Clear relevant modules from cache
        sys.modules.pop(\"myproject.module\", None)
        sys.modules.pop(\"myproject.config\", None)

        from myproject import module  # Fresh import with new env
```

#### Exception Testing Issues
`pytest.raises` may fail with custom exceptions due to module reloading:

```python
# Unreliable with custom exceptions
with pytest.raises(CustomError):
    some_function()

# More reliable approach
try:
    some_function()
    assert False, \"Expected exception but none was raised\"
except Exception as e:
    from myproject.exceptions import CustomError
    assert isinstance(e, (BuiltinError, CustomError)), f\"Unexpected: {type(e)}\"
```

#### Other Common Pitfalls
- **Hypothesis filtering**: Avoid over-filtering strategies; use specific alphabets instead of `assume()` calls
- **Mutable default arguments**: Never use mutable defaults in function signatures
- **Global state pollution**: Always reset global variables/singletons between tests
- **Async testing**: Use `pytest-asyncio` with proper event loop isolation
- **Temporary files**: Use `tempfile.TemporaryDirectory()` for automatic cleanup

### Performance Optimization

#### Identifying Slow Tests
```bash
# Show slowest 10 tests
pytest --durations=10

# Show all test durations (including setup/teardown)
pytest --durations=0 -vv
```

#### Speed Optimization Strategies
1. **Use pytest-xdist for parallel execution**: `pytest -n auto`
2. **Group slow tests with markers**: Mark and run separately
3. **Optimize fixture scope**: Use broader scopes for expensive setups
4. **Mock external dependencies**: Avoid real network/database calls
5. **Use pytest-randomly**: Detect order-dependent tests

### Recommended Pytest Plugins

#### Essential Plugins
- **pytest-cov**: Coverage reporting (`pytest --cov=minerva`)
- **pytest-xdist**: Parallel test execution (`pytest -n auto`)
- **pytest-randomly**: Randomize test order to detect dependencies
- **pytest-clarity**: Better assertion failure messages

#### Development Productivity
- **pytest-watch**: Auto-run tests on file changes
- **pytest-sugar**: Progress bar and better formatting
- **pytest-picked**: Run tests related to unstaged changes
- **pytest-testmon**: Run only tests affected by code changes

#### Specialized Plugins
- **pytest-mock**: Enhanced mock functionality
- **pytest-freezegun**: Mock datetime for time-based tests
- **pytest-benchmark**: Performance benchmarking
- **pytest-timeout**: Prevent hanging tests

### Service Testing with Dependency Injection

```python
# Testing with real ServiceManager
def test_note_creation():
    # Arrange
    service = create_minerva_service()

    # Act
    result = service.note_operations.create_note(\"content\", \"test.md\")

    # Assert
    assert result.exists()

# Testing with mocked dependencies
def test_note_creation_with_mock():
    # Arrange
    mock_file_handler = Mock(spec=FileHandler)
    mock_file_handler.write_file.return_value = Path(\"/test/path.md\")

    service = ServiceManager(config, frontmatter_manager)
    service.note_operations.file_handler = mock_file_handler

    # Act
    result = service.note_operations.create_note(\"content\", \"test.md\")

    # Assert
    mock_file_handler.write_file.assert_called_once()
    assert result == Path(\"/test/path.md\")
```

### CI/CD Testing Best Practices

1. **Fast feedback loop**: Run unit tests first, then integration, then e2e
2. **Fail fast**: Use `--exitfirst` to stop on first failure during development
3. **Parallel execution**: Use `pytest-xdist` in CI for faster runs
4. **Coverage gates**: Enforce minimum coverage thresholds
5. **Marker-based stages**: Run different test types in different CI stages

### See Also
- `docs/test_guidelines.md` for detailed testing patterns and solutions
- `docs/property_based_testing.md` for Hypothesis testing guide
- `.github/workflows/` for CI configuration examples`,
  `old_string`: `## Testing Strategy
- Unit tests for individual functions and service methods
- Integration tests for end-to-end workflows
- **Property-based tests** using Hypothesis for edge case discovery
- Service layer tests with dependency injection
- Mock external dependencies (file system, environment variables)
- Use pytest fixtures for common setup
- Follow AAA pattern: Arrange-Act-Assert with clear section comments
- **Test coverage target**: Maintain 92%+ code coverage
- **Service testing**: Test both service layer and wrapper functions

### Property-Based Testing with Hypothesis
Minerva uses property-based testing to discover edge cases automatically:

- **Target areas**: Path validation, filename validation, tag operations, search functionality
- **Test files**: `tests/*_properties.py` (separate from traditional unit tests)
- **Performance**: ~5-6x slower than unit tests but provides much broader input coverage
- **Edge cases discovered**: Unicode handling, regex escaping, validation order dependencies
- **Documentation**: See `docs/property_based_testing.md` for comprehensive guidelines

**Commands**:
- Run property-based tests: `uv run pytest tests/*_properties.py`
- Reduce examples for CI: `uv run pytest --hypothesis-max-examples=20`
- Debug with seed: `uv run pytest --hypothesis-seed=12345`

### Testing Gotchas ⚠️
- **Module caching issues**: Tests that patch environment variables may need to clear `sys.modules` to ensure fresh imports
- **Exception testing**: `pytest.raises` may fail with custom exceptions; use explicit `try/except` with `isinstance` checks
- **Hypothesis filtering**: Avoid over-filtering strategies; use specific alphabets instead of `assume()` calls
- **See `docs/test_guidelines.md` for detailed solutions and best practices**`

## Python Script Dependencies (PEP 723)

When creating standalone Python scripts that require external dependencies, use PEP 723 inline script metadata to specify dependencies directly in the script file. This eliminates the need for separate requirements.txt files for simple scripts.

### Format:
```python
# /// script
# dependencies = [
#   "requests",
#   "click>=8.0",
#   "pandas>=1.5.0",
# ]
# ///

import requests
import click
import pandas as pd

# Your script code here...
```

### Benefits:

- Self-contained scripts with embedded dependency information
- No need for separate virtual environments or requirements files for simple tasks
- Easy to share and execute with tools that support PEP 723
- Clear dependency tracking at the script level

### When to use:

- One-off automation scripts
- Data processing utilities
- Quick prototypes or proof-of-concepts
- Any standalone script that needs external packages

### Execution:
Scripts with PEP 723 metadata can be executed directly with compatible tools like `pipx run script.py` or other PEP 723-compliant runners.
```
