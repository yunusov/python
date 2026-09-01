import logging
import os

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer
from structlog.stdlib import LoggerFactory


def structlog_configure(logfile: str):
    if logfile:
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            filename="logs/" + logfile,
            encoding="utf-8",
            level=logging.DEBUG,
        )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            get_renderer(logfile),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),
        context_class=dict,
        logger_factory=get_logger_factory(logfile),
        cache_logger_on_first_use=False,
    )


def get_renderer(logfile: str) -> JSONRenderer | ConsoleRenderer:
    """
    Получаем рендерер на основании конфига
    :returns: рендерер structlog
    """

    if logfile:
        return JSONRenderer(ensure_ascii=False)

    return ConsoleRenderer(colors=True)


def get_logger_factory(logfile: str) -> LoggerFactory | structlog.PrintLoggerFactory:
    """
    Получаем логгерфэктори на основании конфига
    :returns: логгерфэктори structlog
    """
    if logfile:
        return LoggerFactory()

    return structlog.PrintLoggerFactory()
