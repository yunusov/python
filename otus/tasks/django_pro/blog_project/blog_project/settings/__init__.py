import os
from pathlib import Path

from dotenv import load_dotenv

from ..loguru_config import AppLogger
from .base import *  # noqa: F401,F403

logger = AppLogger().get_logger()

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
logger.info(f"{ENVIRONMENT=}")

if ENVIRONMENT == "production":
    load_dotenv(BASE_DIR / ".env.production")
    from .production import *  # noqa: F401,F403
else:
    load_dotenv(BASE_DIR / ".env.development")
    from .development import *  # noqa: F401,F403
