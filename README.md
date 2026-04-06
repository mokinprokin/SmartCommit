# 🚀 Smart Commit

[English](README.md) | [Русский](README.ru.md)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)](https://pypi.org/project/smart-commit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Smart Commit** is a robust CLI tool designed to automate and secure your Git workflow. It orchestrates linting, security audits, committing, and pushing into a single, bulletproof operation.

**The Golden Rule:** If your linter fails or secrets are detected, your code doesn't ship.

---

## ✨ Key Features

* 🌍 **Multi-language Support**: Native logs in English and Russian (configurable via `pyproject.toml`).
* 🛡️ **Security Shield**: Automatically scans staged files for API keys, tokens, and secrets. Offers one-click `.gitignore` fixes.
* 🔒 **Branch Guard**: Safeguards `main`, `master`, `prod`, and `release` branches from accidental direct pushes.
* ⚡ **Interactive Flow**: If flags are missing, the tool intelligently prompts you for the branch, message, and remote.
* 🔧 **Zero-Setup**: Works with any stack (Python, JS, Go, Rust, etc.) and is configured via a single standard file.

---

## 📦 Installation

```bash
pip install smart-commit
```

---

## 🔧 Configuration (`pyproject.toml`)

Smart Commit leverages the standard `pyproject.toml` file. Create this section in your project root:

```toml
[tool.smart_commit]
language = "en"  # Supports "en" and "ru"
repository_url = "https://github.com/user/repo.git" # SSH or HTTPS
protected_branches = ["main", "master", "prod"]

# Shell commands to run successfully BEFORE the push.
commands = [
    "ruff check .",      # Python Linter
    "npm run lint",      # Node.js Linter
    "pytest"             # Testing
]
```

---

## 🚀 Usage

Simply run the command in your project root:

```bash
smart-commit
```

### CLI Arguments

If you prefer to bypass the interactive prompts, use these flags:

| Flag | Description |
| --- | --- |
| `-b, --branch` | Target branch name (creates the branch if it doesn't exist) |
| `-m, --message` | Commit message |
| `-r, --remote` | Remote repository name (defaults to `origin`) |

**Example:**
```bash
smart-commit -b feature/auth -m "feat: implement jwt logic" -r origin
```

---

## 🔄 How It Works (The Algorithm)

1.  **Config Loader**: Parses settings and initializes the UI language (EN/RU).
2.  **Branch Guard**: Aborts the operation if you are attempting to push directly to a protected branch.
3.  **Automatic Staging**: Executes `git add .` to prepare your changes.
4.  **Security Scan**: Checks staged files for passwords, tokens, and unignored `.env` files. If a leak is detected, it offers to add them to `.gitignore` automatically.
5.  **Pre-commit Validation**: Sequentially runs your custom `commands`. Any non-zero exit code stops the process to keep your remote history clean.
6.  **Transaction**: Executes `git commit` and `git push` to the specified remote.

---

## 📄 License
Distributed under the MIT License. Feel free to use, modify, and share!
