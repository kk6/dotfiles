# Claude Code Configuration

## User Profile
- **Name**: kk6 (GitHub: https://github.com/kk6)
- **Company**: Web development company using Django primarily

## Technical Stack & Experience Level

### Strong Areas
- **Python**: Intermediate+ (using since 2.x era)
- **Django**: Experienced (since 1.3)
- **Web Development**: Primarily backend

### Learning Areas
- **AWS/Infrastructure**: Beginner level
- **Mathematics**: Middle school level (needs refresher)
- **Frontend**: Company uses jQuery/Bootstrap3, transitioning to Vue, some React experience

### Personal Projects
- Experience with React, TypeScript, Next.js
- Currently working on Minerva project (MCP server for Obsidian)

## Shell Environment (macOS with Homebrew)

### Key Aliases - IMPORTANT for Command Execution
```bash
# Core tools replaced with Rust alternatives
alias ls="lsd"
alias find="fd"  # Use fd instead of find
alias cat="bat"  # Use bat instead of cat
alias tree="lt"  # lsd --tree

# Editor
alias vi="nvim"
alias vim="nvim"

# Git
alias gs="gh copilot suggest"
alias ge="gh copilot explain"

# List variations
alias l="ls -l"
alias ll="l"
alias la="ls -a"
alias lla="ls -la"
alias lt="ls --tree"
```

### Important Notes for AI Agents
- **Always use `fd` instead of `find`** - find is aliased to fd (Rust-based tool)
- **Always use `lsd` instead of `ls`** - ls is aliased to lsd
- **Always use `bat` instead of `cat`** - cat is aliased to bat
- **Use `--no-pager` with git commands** - Pager is enabled by default
- **Use `nvim` for editing** - vi/vim are aliased to nvim

### Installed Tools
- **lsd**: Better ls with colors and icons
- **fd**: Fast find alternative written in Rust
- **bat**: Cat with syntax highlighting
- **rg (ripgrep)**: Fast grep alternative
- **fzf**: Fuzzy finder
- **ghq**: Git repository management
- **zoxide**: Smart cd command
- **starship**: Cross-shell prompt
- **volta**: Node.js version manager

### Environment Paths
```bash
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
export VOLTA_HOME="$HOME/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"
```

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

## Current Projects

### Minerva (Primary Focus)
- **Location**: `/Users/kk6/CascadeProjects/minerva`
- **Repository**: https://github.com/kk6/minerva
- **Description**: MCP server for Obsidian vault management
- **Tech**: Python 3.12+, FastMCP, Pydantic, python-frontmatter
- **Approach**: Document-first development methodology

## Command Examples for AI Agents

### Correct Usage
```bash
# File operations
fd "*.py" src/  # NOT find "*.py" src/
lsd -la         # NOT ls -la
bat file.txt    # NOT cat file.txt

# Git operations
git --no-pager log --oneline
git --no-pager status

# Development
uv run pytest
uv run ruff check src/
```

### Common Mistakes to Avoid
- Don't use `find` - use `fd`
- Don't use raw `ls` - use `lsd` 
- Don't use `cat` - use `bat`
- Don't forget `--no-pager` with git commands
- Don't assume standard GNU tools - many are replaced with Rust alternatives

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
