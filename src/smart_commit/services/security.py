import os
import re
import sys
from .logger import logger
from .i18n import i18n

SECRET_PATTERNS = [
    re.compile(
        r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["\'][a-zA-Z0-9\-_]{10,}["\']'
    ),
    re.compile(r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----"),
]

SUSPICIOUS_FILES = [
    ".env",
    ".env.local",
    "secrets.json",
    ".env.test",
    ".test.env",
    "credentials.json",
]


def check_secrets(staged_files: list[str]) -> bool:
    """
    Проверяет файлы на наличие секретов.
    Возвращает True, если был изменен .gitignore (требуется повторный git add).
    """
    secrets_found = []

    for file_path in staged_files:
        if not os.path.exists(file_path):
            continue

        file_name = os.path.basename(file_path)

        if file_name in SUSPICIOUS_FILES:
            secrets_found.append(file_path)
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if any(pattern.search(content) for pattern in SECRET_PATTERNS):
                    secrets_found.append(file_path)
        except UnicodeDecodeError:
            pass

    if not secrets_found:
        return False

    logger.warning(i18n.t("secret_warn"))
    for s in secrets_found:
        logger.warning(f" -> {s}")

    answer = input(i18n.t("gitignore_ask")).strip().lower()
    if answer == "y":
        with open(".gitignore", "a", encoding="utf-8") as f:
            comment = i18n.t("gitignore_comment")
            f.write(f"\n# {comment}\n")
            for s in secrets_found:
                f.write(f"{s}\n")

        logger.success(i18n.t("gitignore_success"))
        return True

    logger.error(i18n.t("security_abort"))
    sys.exit(1)
