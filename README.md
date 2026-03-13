# 🚀 Smart Commit Tool

Smart Commit Tool is a robust Git wrapper designed for developers who value code quality. It automates the "Pre-check → Commit → Sync → Push" workflow, ensuring that no broken code ever reaches your remote repository.

## ✨ Features

- ⚡ **Automated Validations**: Runs your test suites (Ruff, Pytest, etc.) before every push.
- 🛡️ **Branch Protection**: Prevents accidental pushes to sensitive branches like `main` or `prod`.
- 🔄 **Optimistic Sync**: Automatically handles `pull --rebase` only when conflicts occur, keeping your history clean.
- 🎨 **Terminal UX**: Full color-coded feedback and interactive prompts for a better developer experience.
- ⚙️ **Configurable**: Managed entirely via your existing `pyproject.toml`.

## 📦 Installation

```bash
pip install smart-commit-tool
```

After installation, the `smart-commit` command will be available in your terminal.

## 🔧 Configuration

Add the following section to your `pyproject.toml` to customize the behavior:

```toml
[tool.smart_commit]
repository_url = "https://github.com/youruser/yourrepo.git"
protected_branches = ["main", "master", "prod", "release"]
commands = [
    "ruff check .",
    "pytest",
    ...
]
```

## 🚀 Usage

Simply run the command in your project root:

```bash
smart-commit
```

### CLI Arguments

| Argument      | Description                                       |
|---------------|---------------------------------------------------|
| `-b, --branch`| Specify the target branch (skips interactive prompt) |
| `-m, --message`| Set the commit message (skips interactive prompt) |



### How it works:

1. **Environment Check**: Ensures Git is initialized and the remote URL is correct.
2. **Branch Guard**: If you are on a protected branch, it prompts you to switch to a new one.
3. **Validation**: Runs every command in your `commands` list. If one fails, the process stops.
4. **Smart Push**: Attempts a push. If the remote has changed, it performs a rebase and retries automatically.

## 🛠 Tech Stack

- Python 3.11+
- **Colorama**: For cross-platform terminal styling.
- **Tomli/Tomllib**: For seamless configuration parsing.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
