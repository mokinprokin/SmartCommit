import os
from pathlib import Path
from .logger import logger
from .i18n import i18n

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def load_config() -> dict:
    """Загружает секцию [tool.smart_commit] из pyproject.toml."""
    config_path = Path(os.getcwd()) / "pyproject.toml"

    default_config = {
        "language": "en",
        "repository_url": "",
        "commands": [],
        "protected_branches": ["main", "master", "prod", "release"],
    }

    if not config_path.exists():
        i18n.lang = default_config["language"]
        logger.warning(i18n.t("config_not_found"))
        return default_config

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
            config = data.get("tool", {}).get("smart_commit", default_config)

            i18n.lang = config.get("language", "en")
            return config
    except Exception as e:
        i18n.lang = "en"
        logger.error(i18n.t("config_read_err", e=e))
        return default_config
