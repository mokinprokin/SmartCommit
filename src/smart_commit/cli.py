import subprocess
import sys
import argparse
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def run_shell(command, silent=False):
    """Выполняет консольную команду."""
    if not silent:
        print(f"🛠  Выполняю: {command}")
    result = subprocess.run(command, shell=True, capture_output=silent, text=True)
    return result


def ensure_gitignore():
    """Создает стандартный .gitignore для Python."""
    if not Path(".gitignore").exists():
        print("📝 .gitignore не найден. Создаю стандартный...")
        content = "__pycache__/\n*.py[cod]\n*$py.class\n.venv/\nvenv/\n.env\n.vscode/\ndist/\nbuild/\n*.egg-info/\n"
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(content)


def get_config():
    path = Path("pyproject.toml")
    if not path.exists():
        print("❌ Ошибка: pyproject.toml не найден. Запустите команду в корне проекта.")
        sys.exit(1)

    with open(path, "rb") as f:
        data = tomllib.load(f)
        return data.get("tool", {}).get("smart_commit", {})


def ensure_git_setup(expected_url):
    """Настраивает Git и remote."""
    if not Path(".git").exists():
        print("📁 Git не найден. Инициализирую репозиторий...")
        run_shell("git init")

    res = run_shell("git remote get-url origin", silent=True)
    current_url = res.stdout.strip()

    if res.returncode != 0:
        print(f"🔗 Добавляю remote origin: {expected_url}")
        run_shell(f"git remote add origin {expected_url}")
    elif expected_url not in current_url:
        print(f"🔄 Обновляю URL репозитория на: {expected_url}")
        run_shell(f"git remote set-url origin {expected_url}")
    else:
        print("✅ Git репозиторий настроен.")


def switch_branch(branch):
    """Безопасно переключает ветку, учитывая пустые (unborn) репозитории."""
    has_commits = run_shell("git rev-parse HEAD", silent=True).returncode == 0

    if not has_commits:
        run_shell(f"git branch -M {branch}", silent=True)
    else:
        run_shell(f"git checkout -B {branch}", silent=True)


def main():
    parser = argparse.ArgumentParser(description="Smart Commit & Push Tool")
    parser.add_argument(
        "-b", "--branch", help="Указать ветку (пропустит вопрос о ветке)"
    )
    parser.add_argument(
        "-m", "--message", help="Текст коммита (пропустит вопрос о коммите)"
    )
    args = parser.parse_args()

    config = get_config()
    repo_url = config.get("repository_url")
    commands = config.get("commands", [])

    if not repo_url:
        print(
            "❌ Ошибка: В pyproject.toml не указан [tool.smart_commit].repository_url"
        )
        sys.exit(1)

    ensure_git_setup(repo_url)
    ensure_gitignore()

    print("\n--- 🚀 SMART COMMIT PRE-CHECK ---")

    branch = args.branch
    if not branch:
        current_branch = run_shell(
            "git branch --show-current", silent=True
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
        print("❌ Ошибка: Ветка и сообщение не могут быть пустыми.")
        sys.exit(1)

    switch_branch(branch)

    print("\n--- 🛠 ЗАПУСК ПРОВЕРОК ---")
    for cmd in commands:
        if run_shell(cmd).returncode != 0:
            print(f"\n🛑 Проверка '{cmd}' провалена. Исправь ошибки!")
            sys.exit(1)

    print("\n--- ✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ. ПУШИМ... ---")

    if run_shell("git add .").returncode != 0:
        print("❌ Ошибка при выполнении git add")
        sys.exit(1)

    if run_shell(f'git commit -m "{message}"').returncode != 0:
        print("ℹ️  Нет изменений для коммита или ошибка коммита.")

    print("📥 Синхронизация с GitHub (pull --rebase)...")
    pull_res = run_shell(f"git pull origin {branch} --rebase", silent=True)

    if pull_res.returncode != 0:
        print("🛑 Конфликт при подтягивании изменений!")
        print("Нужно вручную исправить конфликты (git pull) и запустить скрипт снова.")
        sys.exit(1)

    print(f"📤 Отправка изменений в {branch}...")
    push_res = run_shell(f"git push -u origin {branch}")

    if push_res.returncode == 0:
        print(f"\n🎉 Победа! Код проверен, синхронизирован и улетел в '{branch}'.")
    else:
        print("\n❌ Упс! Что-то пошло не так при отправке в Git.")


if __name__ == "__main__":
    main()
