import subprocess
import sys
import argparse
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class SmartCommitError(Exception):
    """Базовый класс для ошибок внутри скрипта."""

    pass


def run_cmd(
    cmd: list[str] | str, silent: bool = False, use_shell: bool = False
) -> subprocess.CompletedProcess[str]:
    """
    Выполняет консольную команду.
    Для внутренних git-команд предпочтительнее передавать список аргументов (use_shell=False).
    """
    if not silent:
        display_cmd = cmd if isinstance(cmd, str) else " ".join(cmd)
        print(f"🛠  Выполняю: {display_cmd}")

    result = subprocess.run(cmd, shell=use_shell, capture_output=silent, text=True)
    return result


def ensure_gitignore() -> None:
    """Создает стандартный .gitignore для Python, если его нет."""
    if not Path(".gitignore").exists():
        print("📝 .gitignore не найден. Создаю стандартный...")
        content = (
            "__pycache__/\n*.py[cod]\n*$py.class\n.venv/\nvenv/\n"
            ".env\n.vscode/\ndist/\nbuild/\n*.egg-info/\n"
        )
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(content)


def get_config() -> dict[str, Any]:
    """Читает конфигурацию из pyproject.toml."""
    path = Path("pyproject.toml")
    if not path.exists():
        raise SmartCommitError(
            "pyproject.toml не найден. Запустите команду в корне проекта."
        )

    with open(path, "rb") as f:
        data = tomllib.load(f)
        return data.get("tool", {}).get("smart_commit", {})


def ensure_git_setup(expected_url: str) -> None:
    """Проверяет и настраивает Git-репозиторий и remote."""
    if not Path(".git").exists():
        print("📁 Git не найден. Инициализирую репозиторий...")
        run_cmd(["git", "init"])

    res = run_cmd(["git", "remote", "get-url", "origin"], silent=True)
    current_url = res.stdout.strip()

    if res.returncode != 0:
        print(f"🔗 Добавляю remote origin: {expected_url}")
        run_cmd(["git", "remote", "add", "origin", expected_url])
    elif expected_url not in current_url:
        print(f"🔄 Обновляю URL репозитория на: {expected_url}")
        run_cmd(["git", "remote", "set-url", "origin", expected_url])
    else:
        print("✅ Git репозиторий настроен.")


def switch_branch(branch: str) -> None:
    """Безопасно переключает ветку, учитывая пустые (unborn) репозитории."""
    has_commits = run_cmd(["git", "rev-parse", "HEAD"], silent=True).returncode == 0

    if not has_commits:
        run_cmd(["git", "branch", "-M", branch], silent=True)
    else:
        run_cmd(["git", "checkout", "-B", branch], silent=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart Commit & Push Tool")
    parser.add_argument(
        "-b", "--branch", help="Указать ветку (пропустит вопрос о ветке)"
    )
    parser.add_argument(
        "-m", "--message", help="Текст коммита (пропустит вопрос о коммите)"
    )
    args = parser.parse_args()

    try:
        config = get_config()
        repo_url = config.get("repository_url")
        commands: list[str] = config.get("commands", [])

        if not repo_url:
            raise SmartCommitError(
                "В pyproject.toml не указан [tool.smart_commit].repository_url"
            )

        ensure_git_setup(repo_url)
        ensure_gitignore()

        print("\n--- 🚀 SMART COMMIT PRE-CHECK ---")

        branch = args.branch
        if not branch:
            current_branch = run_cmd(
                ["git", "branch", "--show-current"], silent=True
            ).stdout.strip()

            if current_branch:
                user_input = input(f"🌿 Ветка [{current_branch}]: ").strip()
                branch = user_input if user_input else current_branch
            else:
                branch = input("🌿 Название ветки (например, main): ").strip()

        message = args.message
        if not message:
            message = input("📝 Сообщение коммита: ").strip()

        if not branch or not message:
            raise SmartCommitError("Ветка и сообщение не могут быть пустыми.")

        switch_branch(branch)

        print("\n--- 🛠 ЗАПУСК ПРОВЕРОК ---")
        for cmd in commands:
            if run_cmd(cmd, use_shell=True).returncode != 0:
                raise SmartCommitError(
                    f"Проверка '{cmd}' провалена. Исправь ошибки и запусти снова!"
                )

        print("\n--- ✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ. ПУШИМ... ---")

        if run_cmd(["git", "add", "."]).returncode != 0:
            raise SmartCommitError("Ошибка при выполнении git add.")

        if run_cmd(["git", "commit", "-m", message]).returncode != 0:
            print("ℹ️  Нет изменений для коммита или ошибка коммита.")

        print(f"📤 Отправка изменений в {branch}...")
        push_res = run_cmd(["git", "push", "-u", "origin", branch], silent=True)

        if push_res.returncode == 0:
            print(f"\n🎉 Победа! Код проверен и улетел в '{branch}'.")
            return

        print("⚠️  Push отклонен. Возможно, на сервере есть новые изменения.")
        print("📥 Запускаю синхронизацию (pull --rebase)...")

        pull_res = run_cmd(["git", "pull", "origin", branch, "--rebase"], silent=True)

        if pull_res.returncode != 0:
            raise SmartCommitError(
                "🛑 Конфликт при подтягивании изменений!\n"
                "Разреши конфликты вручную (git rebase --continue) и попробуй снова."
            )

        print("🔄 Синхронизация прошла успешно. Повторяю push...")
        push_res_retry = run_cmd(["git", "push", "-u", "origin", branch])

        if push_res_retry.returncode == 0:
            print(f"\n🎉 Победа! Изменения синхронизированы и отправлены в '{branch}'.")
        else:
            raise SmartCommitError("Не удалось отправить изменения после rebase.")

    except SmartCommitError as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nОтменено пользователем.")
        sys.exit(0)


if __name__ == "__main__":
    main()
