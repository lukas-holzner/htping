# GitHub Copilot Workspace Instructions

This file contains specific instructions for GitHub Copilot when working in the htping project workspace.

## Quick Reference

### Key Files
- `htping/main.py` - Main CLI application
- `tests/test_main.py` - Unit tests
- `pyproject.toml` - Poetry configuration
- `CONTRIBUTING.md` - Commit message guidelines

### Development Commands
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run htping locally
poetry run htping https://example.com
# Or using the devcontainer alias
htping-dev https://example.com

# Format code
poetry run black htping/ tests/
# Or using the devcontainer alias
format

# Type checking
poetry run mypy htping/
# Or using the devcontainer alias
typecheck

# Linting
lint

# Pre-commit hooks
precommit                    # Run all pre-commit hooks
precommit-update            # Update hook versions
```

## Pre-commit Hooks

The project uses pre-commit hooks for automated code quality checks:
- **Automatic formatting** (Black, isort)
- **Code linting** (flake8)
- **Type checking** (mypy)
- **Commit message validation** (conventional commits)
- **Basic file checks** (trailing whitespace, file endings, etc.)

### Pre-commit Workflow
```bash
# Hooks run automatically on commit
git add .
git commit -m "feat(cli): add new option"
# Hooks run here - if they fail, fix and re-commit

# Manual hook execution
precommit                    # Run all hooks on all files
pre-commit run black         # Run specific hook
```

## Development Environment

### Devcontainer Setup
The project includes a complete devcontainer configuration in `.devcontainer/`:
- **Python 3.12** with Poetry pre-installed
- **All VS Code extensions** for Python development, testing, and GitHub Copilot
- **Automated setup** via post-create script
- **Useful aliases** for common development tasks
- **Pre-configured tools** (Black, MyPy, Flake8, pytest)

### Quick Start with Devcontainer
1. Open project in VS Code
2. Choose "Reopen in Container" when prompted
3. Wait for automatic setup to complete
4. Start coding with all tools ready!

## Code Patterns to Follow

### 1. HTTP Request Handling
Always use this pattern for HTTP requests:
```python
try:
    response = requests.get(url, timeout=10)
    # Process successful response
except requests.RequestException as e:
    # Handle all request-related errors
    print(f"Request failed: {e}")
```

### 2. Statistics Updates
Update global stats dictionary consistently:
```python
stats["transmitted"] += 1
# ... make request ...
stats["received"] += 1
stats["rtt_times"].append(elapsed_time)
```

### 3. Time Measurements
Convert to milliseconds for display:
```python
start_time = time.time()
# ... operation ...
elapsed_time = (time.time() - start_time) * 1000  # ms
```

### 4. CLI Output Format
Follow this format for ping responses:
```python
print(f"{size} bytes from {url}: http_seq={seq} status={status} time={elapsed_time:.2f} ms")
```

## Testing Patterns

### Mock HTTP Requests
```python
def test_successful_request(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.content = b"test content"

    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response

    # Test code here
```

### Test Signal Handling
```python
def test_signal_handler(mocker, capsys):
    mock_exit = mocker.patch('sys.exit')

    # Setup stats
    # Call signal_handler
    # Verify output and exit call
```

## Common Modifications

### Adding CLI Options
1. Add argument to `argparse` configuration in `main()`
2. Pass argument to `htping()` function
3. Update function signature with type hints
4. Add tests for new functionality
5. Update README.md with new option

### Adding New Statistics
1. Add field to global `stats` dictionary
2. Update statistics in request loop
3. Display in `signal_handler`
4. Add tests for new statistic

### Error Handling Improvements
1. Identify specific exception types
2. Add appropriate `except` blocks
3. Provide user-friendly error messages
4. Test error scenarios

## File Templates

### New Test Function
```python
def test_new_functionality(mocker):
    """Test description here."""
    # Arrange
    # Setup mocks and test data

    # Act
    # Call function under test

    # Assert
    # Verify expected behavior
```

### New CLI Option
```python
parser.add_argument(
    '--new-option',
    type=str,
    default='default_value',
    help='Description of the new option'
)
```

## Code Quality Standards

- All functions should have type hints
- Add docstrings for public functions
- Keep functions focused and single-purpose
- Use descriptive variable names
- Handle errors explicitly
- Write tests for new functionality

## Commit Message Examples

```bash
# New feature
git commit -m "feat(cli): add --timeout option for request timeout"

# Bug fix
git commit -m "fix(http): handle connection timeout gracefully"

# Documentation
git commit -m "docs: update README with timeout option"

# Tests
git commit -m "test(cli): add tests for new timeout functionality"
```

Remember to follow the conventional commit format as specified in `CONTRIBUTING.md`.
