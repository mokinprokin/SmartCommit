import argparse
import sys
from .services import (
    config as config_service,
    git as git_service,
    security as security_service,
    runner as runner_service,
)
from .services.logger import logger
from .services.i18n import i18n


def interactive_input(prompt: str, default: str = "") -> str:
    """Запрашивает ввод у пользователя через i18n."""
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value if value else default


def main():
    # 1. Сначала загружаем конфиг, чтобы узнать язык
    config = config_service.load_config()

    # 2. Настройка парсера аргументов
    parser = argparse.ArgumentParser(description="Smart Git Commit Tool")
    parser.add_argument("-b", "--branch", help="Имя ветки")
    parser.add_argument("-m", "--message", help="Сообщение коммита")
    parser.add_argument("-r", "--remote", help="Remote (origin)")

    args = parser.parse_args()

    # 3. Начало работы
    logger.info(i18n.t("init"))

    # Сбор параметров (Fallback на интерактивный ввод с переводами)
    branch = args.branch or interactive_input(i18n.t("branch_prompt"))
    message = args.message or interactive_input(i18n.t("msg_prompt"))
    remote = args.remote or interactive_input(i18n.t("remote_prompt"), default="origin")

    if not branch or not message:
        # Используем новый ключ для ошибки валидации
        logger.error(i18n.t("err_required"))
        sys.exit(1)

    # 4. Валидация и подготовка ветки
    # Передаем список защищенных веток в сервис
    git_service.check_protected(branch, config.get("protected_branches", []))
    git_service.ensure_branch(branch)

    # 5. Индексация файлов
    git_service.add_all()

    # 6. Проверка изменений и безопасность
    staged_files = git_service.get_staged_files()
    if not staged_files:
        logger.warning(i18n.t("no_changes"))
        sys.exit(0)

    # Сканирование на секреты
    if security_service.check_secrets(staged_files):
        # Если секреты найдены и добавлены в .gitignore, пересобираем индекс
        git_service.run_cmd(["git", "rm", "-r", "--cached", "."])
        git_service.add_all()

    # 7. Запуск кастомных команд из pyproject.toml (например, ruff)
    runner_service.run_pre_commands(config.get("commands", []))

    # 8. Финализация
    git_service.commit(message)
    git_service.push(remote, branch)

    logger.success(i18n.t("success"))


if __name__ == "__main__":
    main()
