class I18nService:
    LOCALES = {
        "en": {
            "init": "Initializing Smart Commit...",
            "branch_prompt": "Enter branch name",
            "msg_prompt": "Enter commit message",
            "remote_prompt": "Enter remote",
            "err_required": "Branch and commit message are required!",
            "protected_err": "Direct commit to protected branch '{branch}' is forbidden!",
            "branch_created": "Branch '{branch}' not found. Creating new one...",
            "git_add": "Files added to index (git add).",
            "no_changes": "No changes to commit.",
            "secret_warn": "POSSIBLE SECRET LEAKS DETECTED!",
            "gitignore_ask": "Add these files to .gitignore? [y/N]: ",
            "push_start": "Pushing changes to {remote}/{branch}...",
            "success": "Smart Commit finished successfully!",
            "git_error": "Git Error: {error}",
            "branch_switched": "Switched to branch '{branch}'.",
            "commit_created": "Commit created: '{message}'",
            "push_success": "Push completed successfully!",
            "pre_cmd_start": "Running pre-commit commands...",
            "pre_cmd_exec": "Executing: {cmd}",
            "pre_cmd_err": "Command '{cmd}' failed with error!",
            "pre_cmd_success": "All pre-commit commands executed successfully.",
        },
        "ru": {
            "init": "Инициализация Smart Commit...",
            "branch_prompt": "Введите имя ветки",
            "msg_prompt": "Введите сообщение коммита",
            "remote_prompt": "Введите remote",
            "err_required": "Ветка и сообщение коммита обязательны!",
            "protected_err": "Прямой коммит в защищенную ветку '{branch}' запрещен!",
            "branch_created": "Ветка '{branch}' не найдена. Создаю новую...",
            "git_add": "Файлы добавлены в индекс (git add).",
            "no_changes": "Нет изменений для коммита.",
            "secret_warn": "ОБНАРУЖЕНЫ ВОЗМОЖНЫЕ УТЕЧКИ СЕКРЕТОВ!",
            "gitignore_ask": "Добавить эти файлы в .gitignore? [y/N]: ",
            "push_start": "Отправка изменений в {remote}/{branch}...",
            "success": "Smart Commit успешно завершил работу!",
            "git_error": "Ошибка Git: {error}",
            "branch_switched": "Переключено на ветку '{branch}'.",
            "commit_created": "Коммит создан: '{message}'",
            "push_success": "Push успешно завершен!",
            "pre_cmd_start": "Запуск pre-commit команд...",
            "pre_cmd_exec": "Выполнение: {cmd}",
            "pre_cmd_err": "Команда '{cmd}' завершилась с ошибкой!",
            "pre_cmd_success": "Все pre-commit команды выполнены успешно.",
        },
    }

    def __init__(self, lang="en"):
        self.lang = lang if lang in self.LOCALES else "en"

    def t(self, key, **kwargs):
        """Translate method"""
        text = self.LOCALES[self.lang].get(key, key)
        return text.format(**kwargs)


i18n = I18nService()
