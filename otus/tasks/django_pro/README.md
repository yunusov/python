# Blog API (Django)

Django-приложение блога с моделями постов, комментариев и пользователей, CRUD-функциональностью, Docker-контейнеризацией, PostgreSQL, Redis и Gunicorn.

## Стек технологий

- Python 3.12+
- Django 6.1.2
- Django REST Framework
- PostgreSQL 16
- Redis 8.10.3
- Gunicorn
- Whitenoise (раздача статики в продакшене)
- Loguru (логирование)
- pydantic-settings (конфигурация)
- dj-database-url (настройка БД по URL)
- uv (менеджер пакетов и виртуальных окружений)

## Структура каталогов

```
django_pro/
├── docker-compose.yml        # Окружение: blog, db (PostgreSQL), redis
├── Dockerfile                # Сборка образа приложения (Python 3.12 + uv)
├── entrypoint.sh             # Точка входа контейнера: ожидание БД → миграции → gunicorn
├── gunicorn_config.py        # Конфигурация Gunicorn (хуки, таймауты, логи)
├── start.bat                 # Локальный запуск через runserver (Windows)
├── pyproject.toml            # Зависимости и сборка проекта
├── uv.lock                   # Зафиксированные версии зависимостей
├── .env                      # Переменные окружения (локальные)
├── .env.Example              # Пример заполнения .env
├── .dockerignore
├── blog_project/
│   ├── manage.py             # CLI Django
│   ├── blog_app/             # Приложение блога (модели, представления, URL, миграции)
│   └── blog_project/         # Конфигурация Django
│       ├── settings/         # base.py, development.py, production.py
│       ├── config.py         # Pydantic-настройки (SECRET_KEY, DATABASE_URL и др.)
│       ├── wsgi.py           # WSGI-точка входа
│       └── urls.py           # Основные маршруты
```

## Переменные окружения

Скопируйте `.env.Example` в `.env` и задайте нужные значения:

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `DJANGO_SECRET_KEY` | `django-insecure-default` | Секретный ключ Django |
| `DJANGO_DEBUG` | `False` | Режим отладки |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Разрешённые хосты |
| `DJANGO_DATABASE_URL` | `sqlite:///db.sqlite3` | URL подключения к базе данных |
| `DJANGO_LOG_LEVEL` | `DEBUG` | Уровень логирования |
| `DJANGO_LOG_TO_FILE` | `False` | Писать логи в файл |
| `DJANGO_EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` | Бэкенд почты |
| `REDIS_PASSWORD` | — | Пароль Redis |
| `REDIS_USER` | — | Пользователь Redis |
| `REDIS_USER_PASSWORD` | — | Пароль пользователя Redis |

## Быстрый старт (Docker)

Убедитесь, что установлены Docker и Docker Compose.

```bash
cd j:\dev\python\python\otus\tasks\django_pro

# Скопируйте пример переменных окружения
copy .env.Example .env

# Соберите образы и запустите все сервисы
docker compose up -d --build
```

После запуска приложение будет доступно по адресу:

```
http://127.0.0.1:8000/
```

> ⚠️ Не открывайте `https://127.0.0.1:8000/` — Gunicorn внутри контейнера работает только по HTTP.  
> В `production.py` отключён forced redirect на HTTPS (`SECURE_SSL_REDIRECT = False`), чтобы избежать ошибок SSL при локальной разработке.

Проверьте состояние сервисов:

```bash
docker compose ps
```

Остановить все сервисы:

```bash
docker compose down
```

## Локальный запуск без Docker (Windows)

Требуется [uv](https://github.com/astral-sh/uv).

```bash
# Активируйте виртуальное окружение и установите зависимости
uv sync

# Запустите сервер разработки
python blog_project/manage.py runserver
```

Или используйте готовый скрипт:

```cmd
start.bat
```

Приложение будет доступно по `http://127.0.0.1:8000/`.

## Миграции

Применить миграции к базе данных:

```bash
python blog_project/manage.py migrate
```

Создать новые миграции после изменения моделей:

```bash
python blog_project/manage.py makemigrations blog_app
```

В Docker-контейнере миграции применяются автоматически при старте через `entrypoint.sh` (после того, как PostgreSQL станет доступен).

## Статика

Собрать статические файлы в `STATIC_ROOT` (используется Whitenoise):

```bash
python blog_project/manage.py collectstatic --noinput
```

Эта команда уже выполняется при сборке Docker-образа.

## Healthcheck

Доступен эндпоинт:

```
GET http://127.0.0.1:8000/health/
```

Ответ:

```json
{"status": "ok"}
```

Он используется в `docker-compose.yml` для проверки работоспособности контейнера `blog` (инструкция `healthcheck`).

## Остановка и удаление контейнеров

```bash
docker compose down
```

Если нужно удалить также именованные тома (данные PostgreSQL и Redis):

```bash
docker compose down -v
```

## Важные замечания

1. **SIGTERM / graceful shutdown** — у сервиса `blog` установлен `stop_grace_period: 120s` и `restart: unless-stopped`. При остановке Gunicorn корректно завершает воркеры.
2. **Сигналы и очистка ресурсов** — при завершении процесса закрываются соединения с базой данных (`connections.close_all()`) и обработчики Loguru.
3. **Redis** — контейнер `redis_container` запускается с ACL и паролем из `.env`. Данные хранятся в папке `redisdata/`.
4. **PostgreSQL** — данные хранятся в именованном томе `postgres_data`.

## Разработка

При внесении изменений в модели не забудьте:

1. Создать миграцию: `makemigrations`
2. Применить её: `migrate`
3. Собрать статику: `collectstatic --noinput`
4. Пересобрать Docker-образ: `docker compose build blog`
