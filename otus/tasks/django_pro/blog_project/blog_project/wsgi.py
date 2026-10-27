"""
WSGI config for blog_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import atexit
import logging
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

application = get_wsgi_application()

logger = logging.getLogger(__name__)

def _cleanup(signum=None, frame=None):
    """Очистка ресурсов при завершении процесса."""
    logger.info("Cleanup started...")

    # Закрываем соединения с базой данных
    try:
        from django.db import connections
        connections.close_all()
    except Exception as exc:
        logger.warning(f"Could not close DB connections: {exc}")

    # Закрываем соединение с Redis (если используется django-redis)
    try:
        from django_redis import get_redis_connection
        get_redis_connection().close()
    except NotImplementedError:
        # Этот бэкенд не поддерживает close() — игнорируем
        pass
    except Exception as exc:
        logger.warning(f"Could not close Redis connection: {exc}")

    # Удаляем обработчики loguru
    try:
        from .loguru_config import AppLogger
        loguru_logger = AppLogger().get_logger()
        loguru_logger.info("AppLogger cleanup")
        loguru_logger.remove()
    except Exception as exc:
        logger.warning(f"loguru exception: {exc}")

    logger.info("Cleanup complete")

# Регистрируем для обычного выхода Python
atexit.register(_cleanup)

# Регистрируем для SIGINT (Ctrl+C) и SIGTERM (docker stop)
import signal

signal.signal(signal.SIGINT, _cleanup)
signal.signal(signal.SIGTERM, _cleanup)
