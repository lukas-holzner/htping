# GitHub Copilot Instructions for htping

## Project Context

htping is a Python CLI tool that functions as an HTTP version of the traditional `ping` command. It sends periodic HTTP GET requests to monitor website availability and responsiveness.

## Project Structure

- `htping/main.py` - Core CLI functionality with HTTP request handling
- `tests/test_main.py` - Unit tests with pytest and mocking
- `pyproject.toml` - Poetry configuration and dependencies
- Uses semantic-release for automated versioning

## Code Style Guidelines

### Python Code Standards

1. **Follow PEP 8** for Python code formatting
2. **Use type hints** where appropriate, especially for function parameters and return types
3. **Docstrings** should follow Google style for functions and classes
4. **Error handling** should be explicit with appropriate exception types
5. **Import organization**: standard library, third-party, local imports (separated by blank lines)

### Specific Patterns for htping

1. **HTTP requests**: Always use the `requests` library with proper exception handling
2. **Time measurements**: Use `time.time()` and convert to milliseconds for consistency
3. **Statistics tracking**: Update the global `stats` dictionary for transmitted/received counts
4. **Signal handling**: Graceful shutdown with Ctrl+C should display statistics
5. **CLI arguments**: Use `argparse` with clear help descriptions

### Testing Patterns

1. **Use pytest** as the testing framework
2. **Mock external dependencies** (especially HTTP requests) using `pytest-mock`
3. **Test both success and failure scenarios** for HTTP requests
4. **Test signal handling** and statistics output
5. **Parametrize tests** when testing multiple similar scenarios

## Code Examples

### Function Definition with Type Hints
```python
def htping(url: str, interval: float, count: Optional[int] = None) -> None:
    """Send HTTP requests to a URL at regular intervals.

    Args:
        url: The target URL to ping
        interval: Time in seconds between requests
        count: Optional limit on number of requests
    """
```

### Error Handling Pattern
```python
try:
    response = requests.get(url)
    # Handle success
except requests.RequestException as e:
    # Handle failure
    print(f"Request failed: {e}")
```

### Test Structure
```python
def test_function_name(mocker):
    # Arrange
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200

    # Act
    result = function_under_test()

    # Assert
    assert expected_result == result
    mock_get.assert_called_once()
```

## Dependencies and Tools

- **Python 3.10+** required
- **requests** for HTTP functionality
- **pytest** and **pytest-mock** for testing
- **Poetry** for dependency management
- **semantic-release** for automated releases

## Common Tasks

1. **Adding new CLI options**: Extend the `argparse` configuration in `main()`
2. **Modifying HTTP behavior**: Update the `htping()` function
3. **Adding statistics**: Extend the global `stats` dictionary
4. **Adding tests**: Create new test functions in `tests/test_main.py`

## Performance Considerations

- Keep the tool lightweight and fast
- Minimize memory usage for long-running sessions
- Handle network timeouts gracefully
- Avoid blocking operations in the main loop

## Security Considerations

- Validate URLs before making requests
- Handle malformed responses safely
- Consider rate limiting for responsible usage
- Sanitize any user input that gets logged
