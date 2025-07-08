#!/bin/bash

# Post-create script for htping devcontainer
# This script runs after the container is created to set up the development environment

set -e

echo "🚀 Setting up htping development environment..."

# Configure zsh and oh-my-zsh
echo "🐚 Configuring zsh and oh-my-zsh..."
# Enable git plugin in oh-my-zsh
sed -i 's/plugins=(git)/plugins=(git)/' ~/.zshrc

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update

# Install Poetry
echo "📝 Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/vscode/.local/bin:$PATH"
echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> ~/.zshrc

# Configure Poetry
echo "⚙️ Configuring Poetry..."
poetry config virtualenvs.create false

# Install project dependencies
echo "📚 Installing project dependencies..."
poetry install

# Install Node.js dependencies for semantic-release
echo "🌟 Installing Node.js dependencies..."
npm install

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
echo "✅ Pre-commit hooks installed successfully!"

# Set up Git configuration helpers
echo "🔧 Setting up Git helpers..."
git config --global --add safe.directory /workspaces/htping

# Create useful aliases
echo "🎯 Setting up useful aliases..."
echo 'alias htping-dev="poetry run python -m htping.main"' >> ~/.bashrc
echo 'alias test="poetry run pytest"' >> ~/.bashrc
echo 'alias test-watch="poetry run pytest-watch"' >> ~/.bashrc
echo 'alias lint="poetry run flake8 htping/ tests/"' >> ~/.bashrc
echo 'alias format="poetry run black htping/ tests/"' >> ~/.bashrc
echo 'alias typecheck="poetry run mypy htping/"' >> ~/.bashrc
echo 'alias precommit="pre-commit run --all-files"' >> ~/.bashrc
echo 'alias precommit-update="pre-commit autoupdate"' >> ~/.bashrc

# Also add aliases to zsh
echo 'alias htping-dev="poetry run python -m htping.main"' >> ~/.zshrc
echo 'alias test="poetry run pytest"' >> ~/.zshrc
echo 'alias test-watch="poetry run pytest-watch"' >> ~/.zshrc
echo 'alias lint="poetry run flake8 htping/ tests/"' >> ~/.zshrc
echo 'alias format="poetry run black htping/ tests/"' >> ~/.zshrc
echo 'alias typecheck="poetry run mypy htping/"' >> ~/.zshrc
echo 'alias precommit="pre-commit run --all-files"' >> ~/.zshrc
echo 'alias precommit-update="pre-commit autoupdate"' >> ~/.zshrc

# Make the htping command available for development
echo "🔗 Setting up development symlink..."
poetry install

# Display useful information
echo ""
echo "✅ htping development environment setup complete!"
echo ""
echo "📋 Available commands:"
echo "  htping-dev <url>     - Run htping in development mode"
echo "  test                 - Run test suite"
echo "  lint                 - Run code linting"
echo "  format               - Format code with Black"
echo "  typecheck            - Run type checking with mypy"
echo "  precommit            - Run all pre-commit hooks"
echo "  precommit-update     - Update pre-commit hook versions"
echo ""
echo "🎉 Happy coding!"
echo ""

# Test installation
echo "🧪 Testing installation..."
poetry run python -c "import htping; print('✅ htping module imported successfully')"
poetry run pytest --version
echo "✅ All tools are working correctly!"
