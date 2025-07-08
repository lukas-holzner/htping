# htping Devcontainer Configuration

This directory contains the development container configuration for the htping project, providing a consistent and fully-configured development environment.

## What's Included

### Base Environment
- **Python 3.12** with Poetry for dependency management
- **Node.js LTS** for semantic-release and build tools
- **Git** and **GitHub CLI** for version control and repository management

### VS Code Extensions
- **Python Development**: Python extension pack with linting, formatting, and testing
- **Code Quality**: Black formatter, Pylint, Flake8, MyPy type checker
- **GitHub Copilot**: AI-powered code assistance and chat
- **Testing**: Python test adapter for integrated test running
- **Markdown**: Markdown editing and linting support
- **Git**: GitLens for enhanced Git integration

### Pre-configured Tools
- **Poetry**: Python dependency management and packaging
- **pytest**: Testing framework with automatic discovery
- **Black**: Code formatting with 88-character line length
- **MyPy**: Static type checking
- **Flake8**: Code linting and style checking

## Quick Start

1. **Open in VS Code**: Use the "Reopen in Container" prompt or Command Palette
2. **Wait for setup**: The post-create script will automatically install dependencies
3. **Start coding**: All tools are pre-configured and ready to use

## Available Commands

The devcontainer sets up useful aliases for common development tasks:

```bash
# Development
htping-dev https://example.com    # Run htping in development mode
poetry run htping https://example.com  # Alternative way to run

# Testing
test                              # Run all tests
test-watch                        # Run tests in watch mode
poetry run pytest tests/         # Run tests with full output

# Code Quality
format                            # Format code with Black
lint                              # Run Flake8 linting
typecheck                         # Run MyPy type checking

# Project Management
poetry install                    # Install/update dependencies
poetry add <package>              # Add new dependency
poetry build                      # Build distribution packages
```

## Development Workflow

1. **Make changes** to code in `htping/` or tests in `tests/`
2. **Format code** with `format` command
3. **Run tests** with `test` command
4. **Check types** with `typecheck` command
5. **Commit** using conventional commit format (see `CONTRIBUTING.md`)

## VS Code Integration

### Testing
- Tests appear in the Test Explorer sidebar
- Run individual tests or test files directly from the editor
- Debug tests with breakpoints

### Code Quality
- Format on save is enabled
- Import organization on save
- Real-time linting and type checking
- Problems panel shows all issues

### GitHub Copilot
- Code suggestions and completions
- Chat interface for code questions
- Follows project-specific instructions in `.github/copilot-*.md`

## Troubleshooting

### Container Won't Start
- Check Docker is running
- Verify VS Code has the Dev Containers extension
- Try rebuilding the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

### Dependencies Missing
- Rebuild container or run `poetry install` manually
- Check the post-create script logs in the terminal

### Tests Not Running
- Ensure pytest is installed: `poetry run pytest --version`
- Check test discovery: `poetry run pytest --collect-only`
- Verify test files are in the `tests/` directory

### Type Checking Issues
- Install type stubs: `poetry add --group dev types-requests`
- Check MyPy configuration in `pyproject.toml`

## Customization

### Adding Extensions
Edit `.devcontainer/devcontainer.json` and add extension IDs to the `extensions` array.

### Modifying Settings
Update the `settings` section in `devcontainer.json` for VS Code configuration.

### Additional Dependencies
- Python packages: Add to `pyproject.toml` and run `poetry install`
- System packages: Add to `post-create.sh` with `apt-get install`
- Node packages: Add to `package.json` and run `npm install`

## Performance Tips

- The container mounts the `.git` directory for performance
- Use the integrated terminal for Git operations
- Large dependency changes may require container rebuild
