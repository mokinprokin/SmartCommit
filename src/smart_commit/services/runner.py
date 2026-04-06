import subprocess
import sys
from .logger import logger
from .i18n import i18n


def run_pre_commands(commands: list[str]):
    """Запускает команды из конфига перед коммитом."""
    if not commands:
        return

    logger.info(i18n.t("pre_cmd_start"))
    for cmd in commands:
        logger.info(i18n.t("pre_cmd_exec", cmd=cmd))
        result = subprocess.run(cmd, shell=True)

        if result.returncode != 0:
            logger.error(i18n.t("pre_cmd_err", cmd=cmd))
            sys.exit(1)

    logger.success(i18n.t("pre_cmd_success"))
