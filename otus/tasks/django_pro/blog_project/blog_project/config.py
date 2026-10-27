import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("DJANGO_SECRET_KEY", "django-insecure-default")
    DEBUG: bool = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
    ALLOWED_HOSTS: list = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")]
    DATABASE_URL: str = os.getenv("DJANGO_DATABASE_URL", "sqlite:///db.sqlite3")
    LOG_LEVEL: str = os.getenv("DJANGO_LOG_LEVEL", "DEBUG")
    LOG_TO_FILE: bool = os.getenv("DJANGO_LOG_TO_FILE", "False").lower() == "true"
    EMAIL_BACKEND: str = os.getenv("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

settings = Settings()
