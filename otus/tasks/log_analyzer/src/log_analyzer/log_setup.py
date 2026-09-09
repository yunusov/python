import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer
from structlog.stdlib import LoggerFactory

TOP_FOLDER = Path(__file__).resolve().parent.parent.parent

APP_LOGGER = "log_analyzer"


def structlog_configure(logfile: str):
    if logfile:
        os.makedirs("logs", exist_ok=True)
        _setup_file_handler(APP_LOGGER, TOP_FOLDER / f"logs/{logfile}")

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            get_renderer(logfile),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(min_level=logging.DEBUG),
        context_class=dict,
        logger_factory=get_logger_factory(logfile),
        cache_logger_on_first_use=False,
    )
    if logfile:
        logging.getLogger(APP_LOGGER).info("Логгер настроен, пишем в logs/%s", logfile)


def _setup_file_handler(logger_name: str, filename: Path) -> None:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    handler = RotatingFileHandler(
        filename=filename,
        maxBytes=10 * 1024 * 1024,  # 10 МБ
        backupCount=5,  # logg.log, logg.log.1 … logg.log.5
        encoding="utf-8",
    )
    logger.addHandler(handler)
    logger.propagate = False


def get_renderer(logfile: str) -> JSONRenderer | ConsoleRenderer:
    """
    Получаем рендерер на основании конфига
    :returns: рендерер structlog
    """

    if logfile:
        return JSONRenderer(ensure_ascii=False)

    return ConsoleRenderer(colors=False)


def get_logger_factory(logfile: str) -> LoggerFactory | structlog.PrintLoggerFactory:
    """
    Получаем логгерфэктори на основании конфига
    :returns: логгерфэктори structlog
    """
    if logfile:
        return LoggerFactory()

    return structlog.PrintLoggerFactory()
