import subprocess
import sys
from .logger import logger
from .i18n import i18n


def run_cmd(cmd: list[str], check=True) -> str:
    """Выполняет bash-команду и возвращает вывод."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        error_msg = result.stderr.strip()
        logger.error(i18n.t("git_error", error=error_msg))
        sys.exit(1)
    return result.stdout.strip()


def check_protected(branch: str, protected_branches: list[str]):
    """Блокирует пуш в защищенные ветки."""
    if branch in protected_branches:
        logger.error(i18n.t("protected_err", branch=branch))
        sys.exit(1)


def ensure_branch(branch: str):
    """Проверяет наличие ветки. Если нет - создает."""
    result = subprocess.run(["git", "checkout", branch], capture_output=True, text=True)
    if result.returncode != 0:
        logger.info(i18n.t("branch_created", branch=branch))
        run_cmd(["git", "checkout", "-b", branch])
    else:
        logger.info(i18n.t("branch_switched", branch=branch))


def add_all():
    run_cmd(["git", "add", "."])
    logger.info(i18n.t("git_add"))


def get_staged_files() -> list[str]:
    """Возвращает список файлов, готовых к коммиту."""
    output = run_cmd(["git", "diff", "--cached", "--name-only"])
    return [f for f in output.split("\n") if f]


def commit(message: str):
    run_cmd(["git", "commit", "-m", message], check=False)
    logger.info(i18n.t("commit_created", message=message))


def push(remote: str, branch: str):
    logger.info(i18n.t("push_start", remote=remote, branch=branch))
    run_cmd(["git", "push", "-u", remote, branch])
    logger.success(i18n.t("push_success"))
