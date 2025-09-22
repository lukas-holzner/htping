# Pre-commit Hooks for hping

This project uses [pre-commit](https://pre-commit.com/) to ensure code quality and consistency before commits reach the repository.

## What Gets Checked

### Code Formatting

- **Black**: Automatic Python code formatting (88 character line length)
- **isort**: Import sorting and organization

### Code Quality

- **flake8**: Style guide enforcement and error detection
- **mypy**: Static type checking

### Basic Checks

- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML file syntax
- **check-toml**: Validates TOML file syntax (pyproject.toml)
- **check-merge-conflict**: Detects merge conflict markers
- **check-added-large-files**: Prevents large files from being committed
- **debug-statements**: Detects debug statements (pdb, print, etc.)

### Commit Message Validation

- **conventional-pre-commit**: Enforces conventional commit format
  - Examples: `feat:`, `fix:`, `docs:`, `refactor:`, etc.
  - See `CONTRIBUTING.md` for full commit message guidelines

## How It Works

### Automatic Execution

Pre-commit hooks run automatically when you commit:

```bash
git add .
git commit -m "feat(cli): add timeout option"
# Hooks run automatically here
```

If any hook fails:

1. The commit is blocked
2. Issues are automatically fixed where possible
3. You need to re-add and commit the fixed files

### Example Workflow

```bash
# Make changes to code
echo "import os,sys" > test.py  # Bad import formatting

# Try to commit
git add test.py
git commit -m "feat: add test file"

# isort will fix the imports automatically:
# import os
# import sys

# Re-add the fixed file and commit
git add test.py
git commit -m "feat: add test file"
# ✅ Commit succeeds
```

## Manual Control

### Run All Hooks

```bash
# Run on all files
precommit

# Or using full command
pre-commit run --all-files
```

### Run Specific Hooks

```bash
# Format code
pre-commit run black

# Check types
pre-commit run mypy

# Sort imports
pre-commit run isort
```

### Update Hook Versions

```bash
# Update to latest versions
precommit-update

# Or using full command
pre-commit autoupdate
```

### Skip Hooks (Emergency Only)

```bash
# Skip all hooks - not recommended!
git commit --no-verify -m "emergency fix"

# Skip specific hooks
SKIP=mypy git commit -m "fix: urgent bug fix"
```

## Configuration

### Pre-commit Config (`.pre-commit-config.yaml`)

- Defines which hooks to run and their versions
- Automatically updated with `pre-commit autoupdate`

### Tool Settings (`pyproject.toml`)

- **Black**: 88 character line length, Python 3.10+ target
- **isort**: Black-compatible profile, recognizes hping as first-party
- **mypy**: Strict type checking with test exceptions
- **flake8**: Compatible with Black formatting

## Benefits

### For Developers

- **Automatic formatting**: No manual `black` or `isort` commands needed
- **Catch errors early**: Find issues before CI/CD
- **Consistent style**: All contributors follow same standards
- **Faster reviews**: Less time spent on style feedback

### For the Project

- **Higher code quality**: Prevents style and quality issues
- **Reliable commits**: Every commit passes basic quality checks
- **Automated enforcement**: No manual enforcement needed
- **CI/CD optimization**: Fewer failed builds due to style issues

## Troubleshooting

### Hook Installation Issues

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
pre-commit install --hook-type commit-msg
```

### Performance Issues

```bash
# Clean hook cache
pre-commit clean

# Reinstall all hooks
pre-commit install-hooks
```

### Persistent Failures

```bash
# See detailed output
pre-commit run --verbose

# Debug specific hook
pre-commit run mypy --verbose
```

### Disable Temporarily

```bash
# Disable all hooks temporarily
pre-commit uninstall

# Re-enable later
pre-commit install
pre-commit install --hook-type commit-msg
```

## Integration with Development Workflow

### VS Code Integration

The devcontainer automatically installs and configures pre-commit hooks. They work seamlessly with:

- Format on save (runs Black)
- Integrated terminal commits
- Source control panel commits

### Poetry Integration

All hooks respect Poetry's virtual environment and use the correct Python interpreter and dependencies.

### CI/CD Integration

Pre-commit hooks complement (not replace) GitHub Actions CI checks. They catch issues locally before pushing to remote.

## Best Practices

1. **Let hooks fix what they can**: Don't fight the auto-formatting
2. **Review auto-fixes**: Understand what the hooks changed
3. **Use meaningful commit messages**: Follow conventional commit format
4. **Update regularly**: Run `precommit-update` occasionally
5. **Don't skip hooks**: Only use `--no-verify` in true emergencies

Pre-commit hooks are your first line of defense for code quality. They save time, prevent errors, and ensure consistency across the entire hping project.
