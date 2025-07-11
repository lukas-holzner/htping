# 🌐 htping - Ping but for HTTP

<div align="center">

[![Release](https://github.com/lukas-holzner/htping/actions/workflows/release.yml/badge.svg)](https://github.com/lukas-holzner/htping/actions/workflows/release.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![PyPI Version](https://img.shields.io/pypi/v/htping.svg)](https://pypi.org/project/htping/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PyPI Downloads](https://img.shields.io/pypi/dm/htping.svg)](https://pypi.org/project/htping/)
[![GitHub Stars](https://img.shields.io/github/stars/lukas-holzner/htping.svg)](https://github.com/lukas-holzner/htping/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/lukas-holzner/htping.svg)](https://github.com/lukas-holzner/htping/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/lukas-holzner/htping.svg)](https://github.com/lukas-holzner/htping/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/lukas-holzner/htping.svg)](https://github.com/lukas-holzner/htping/pulls)

</div>

`htping` is a command-line tool that works like `ping`, but instead of sending ICMP packets, it repeatedly makes HTTP GET requests to check if a website is available.

## ✨ Key Features

- 🔄 **Continuous monitoring** - Send periodic HTTP requests like traditional ping
- 📊 **Real-time statistics** - View response times, success rates, and packet loss
- ⚡ **Lightweight & fast** - Minimal resource usage with quick response times
- 🎯 **Simple interface** - Familiar ping-like command-line experience
- 🐍 **Python 3.10+** - Modern Python with type hints and clean code

## 📦 Installation

### Requirements
- Python 3.10 or higher
- Internet connection

### Install from PyPI
```bash
pip install htping
```

### Install from Source
```bash
git clone https://github.com/lukas-holzner/htping.git
cd htping
poetry install
```


## 🚀 Usage

To use `htping`, simply run it from the command line followed by the URL you want to ping:

```bash
htping https://www.example.com
```

## ⚙️ Options

- `-i`, `--interval`: Interval in seconds between requests (default is 1.0 seconds).
- `-c`, `--count`: Number of pings to send. (default is none)

## 💡 Example

```bash
htping https://www.example.com -i 2
```

This will send HTTP GET requests to `https://www.example.com` every 2 seconds.

## 📋 About

`htping` is a simple tool for monitoring the availability and responsiveness of websites by sending periodic HTTP GET requests.

## 🛠️ Development

For development setup with devcontainer support and pre-commit hooks, see `CONTRIBUTING.md`.

### Quick Development Setup
```bash
# Using devcontainer (recommended)
# Open in VS Code and select "Reopen in Container"

# Or manual setup
poetry install
pre-commit install
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

- Check out the [Contributing Guide](CONTRIBUTING.md) for development setup
- Browse [open issues](https://github.com/lukas-holzner/htping/issues) for ways to help
- Read about our [commit conventions](CONTRIBUTING.md#commit-message-guidelines)

## 📄 License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.

## 🌟 Support

If you find this tool useful, please consider:
- ⭐ Starring the repository
- 🐛 [Reporting issues](https://github.com/lukas-holzner/htping/issues)
- 💡 [Suggesting enhancements](https://github.com/lukas-holzner/htping/issues)
- 📢 Sharing with others
