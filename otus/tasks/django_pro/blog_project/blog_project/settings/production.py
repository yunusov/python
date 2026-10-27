import os

from ..config import settings
from .base import DATABASES, INSTALLED_APPS, MIDDLEWARE

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
DEBUG=False

INSTALLED_APPS = INSTALLED_APPS + ['whitenoise.runserver_nostatic']
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "False").lower() == "true"


LOGGING = {
    'version': 1,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',  # опционально, если добавите зависимость
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',  # structured JSON logs
        },
    },
    'root': {
        'handlers': ['console'],
        'level': settings.LOG_LEVEL,
    },
}

DATABASES = {
    'default': {
        **DATABASES['default'],
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}

SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
