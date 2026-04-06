# 🚀 Smart Commit

[English](README.md) | [Русский](README.ru.md)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)](https://pypi.org/project/smart-commit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Smart Commit** — это CLI-инструмент для автоматизации Git-воркфлоу. Он объединяет линтинг, проверку безопасности, коммит и пуш в одну безопасную операцию.

**Главное правило:** Если линтер нашел ошибку или в коде есть секреты — пуш будет заблокирован.

---

## ✨ Ключевые фишки

* 🌍 **Мультиязычность**: Поддержка логов на русском и английском (настраивается в `pyproject.toml`).
* 🛡️ **Security Shield**: Автоматический поиск API-ключей и секретов перед коммитом. Предлагает добавить их в `.gitignore` в один клик.
* 🔒 **Branch Guard**: Защита веток `main`, `master`, `prod`, `release` от прямого пуша.
* ⚡ **Interactive Flow**: Если флаги не указаны, инструмент сам спросит ветку, сообщение и remote.
* 🔧 **Zero-setup**: Работает с любым стеком (Python, JS, Go и др.), настраивается через один файл.

---

## 📦 Установка

```bash
pip install smart-commit-tool
```

---

## 🔧 Конфигурация (`pyproject.toml`)

Smart Commit использует стандартный файл `pyproject.toml`. Создайте его в корне вашего проекта:

```toml
[tool.smart_commit]
language = "ru"  # Поддерживается "ru" и "en"
repository_url = "https://github.com/user/repo.git" # Можно SSH или HTTPS
protected_branches = ["main", "master", "prod"]

# Команды, которые должны выполниться УСПЕШНО перед пушем
commands = [
    "ruff check .",      # Python линтер
    "npm run lint"       # Node.js линтер
]
```

---

## 🚀 Использование

Просто запустите команду в корне проекта:

```bash
smart-commit
```

### Флаги командной строки

Если вы не хотите использовать интерактивный ввод, передайте аргументы:

| Флаг | Описание |
| --- | --- |
| `-b, --branch` | Имя целевой ветки (если ветки нет — будет создана) |
| `-m, --message` | Сообщение коммита |
| `-r, --remote` | Имя удаленного репозитория (по умолчанию `origin`) |

**Пример:**
```bash
smart-commit -b feature/login -m "feat: add auth logic" -r origin
```

---

## 🔄 Как это работает (Алгоритм)

1.  **Загрузка конфига**: Читает настройки и устанавливает язык (RU/EN).
2.  **Проверка ветки**: Если вы в защищенной ветке — выполнение прерывается.
3.  **Индексация**: Автоматический `git add .`.
4.  **Security Scan**: Проверяет измененные файлы на наличие паролей, токенов и `.env` файлов. Если найдено — предлагает мгновенно добавить их в `.gitignore`.
5.  **Pre-commit Check**: Запускает ваши команды из `commands`. Любая ошибка (exit code != 0) остановит процесс.
6.  **Транзакция**: Выполняет `git commit` и `git push` в указанный remote.

---

## 📄 Лицензия
Распространяется под лицензией MIT. Пользуйтесь, дорабатывайте и делитесь!
