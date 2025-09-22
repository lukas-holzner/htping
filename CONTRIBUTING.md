# Commit Message Guidelines for hping

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for standardized commit messages that enable automated semantic versioning and changelog generation.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

### Main Types

- **feat**: A new feature for the user
- **fix**: A bug fix for the user
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semi-colons, etc)
- **refactor**: Code changes that neither fix a bug nor add a feature
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates, build changes

### Special Types

- **perf**: Performance improvements
- **ci**: Changes to CI/CD configuration
- **build**: Changes to build system or external dependencies
- **revert**: Reverts a previous commit

## Scopes (Optional)

Common scopes for hping:

- **cli**: Command-line interface changes
- **http**: HTTP request handling
- **stats**: Statistics and metrics
- **tests**: Test-related changes
- **deps**: Dependency updates
- **release**: Release-related changes

## Breaking Changes

For breaking changes, add `!` after the type/scope:

```
feat!: remove deprecated --timeout option
```

Or add `BREAKING CHANGE:` in the footer:

```
feat: add new authentication method

BREAKING CHANGE: The --auth flag now requires username:password format
```

## Examples

### Feature Addition

```
feat(cli): add --timeout option for request timeout

Add a new command-line option to specify HTTP request timeout.
Default timeout is set to 10 seconds.

Closes #42
```

### Bug Fix

```
fix(http): handle connection timeout gracefully

Previously, connection timeouts would crash the application.
Now they are caught and displayed as failed requests.

Fixes #38
```

### Documentation Update

```
docs: update README with new timeout option

Add documentation for the new --timeout flag and update
usage examples.
```

### Refactoring

```
refactor(stats): extract statistics display into separate function

Move statistics formatting logic from signal_handler to
a dedicated display_stats function for better testability.
```

### Test Addition

```
test(http): add tests for timeout handling

Add unit tests to verify proper handling of connection
timeouts and request failures.
```

### Dependency Update

```
chore(deps): update requests to 2.31.0

Update requests library to latest version for security fixes.
```

### Performance Improvement

```
perf(http): reduce memory usage for large responses

Only read response headers for size calculation instead
of loading entire response body into memory.
```

### CI/CD Changes

```
ci: add Python 3.12 to test matrix

Extend automated testing to include Python 3.12 compatibility.
```

## Semantic Release Impact

The commit types trigger different version bumps:

- **feat**: Minor version bump (0.2.6 → 0.3.0)
- **fix**: Patch version bump (0.2.6 → 0.2.7)
- **BREAKING CHANGE**: Major version bump (0.2.6 → 1.0.0)
- **docs**, **style**, **refactor**, **test**, **chore**: No version bump

## Best Practices

1. **Use imperative mood**: "add feature" not "added feature"
2. **Keep subject line under 50 characters**
3. **Capitalize the subject line**
4. **Don't end subject line with a period**
5. **Use body to explain what and why, not how**
6. **Reference issues and PRs when applicable**

### Good Examples

```
feat: add request retry mechanism
fix: prevent crash on invalid URL
docs: add installation instructions
```

### Bad Examples

```
Added new feature  # Past tense, not descriptive
fix bug            # Too vague
Update README.md   # Not following convention
```

## Tools and Automation

- **semantic-release** automatically generates versions and changelogs
- **commitizen** can help format commits: `npm install -g commitizen`
- **GitHub Actions** validates commit messages in CI

## Pre-commit Checklist

Before committing:

- [ ] Commit message follows conventional format
- [ ] Type accurately describes the change
- [ ] Description is clear and concise
- [ ] Breaking changes are properly marked
- [ ] Related issues are referenced
- [ ] Tests pass locally
