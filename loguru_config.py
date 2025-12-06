# pip install loguru

import sys
import os
from loguru import logger

def setup_logging():
    """
    Настраивает логгер для всего приложения в зависимости от окружения.
    """
    # Удаляем стандартный обработчик, чтобы избежать дублирования
    logger.remove()

    # Определяем формат для консоли (разработка)
    dev_format = (
        "DEV~<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{file}:{line}</cyan>_<cyan>{function}</cyan> - <level>{message}</level>"
    )

    # Определяем формат для файла (продакшен)
    prod_format = "PROD~{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    # Конфигурация для разработки (если не указано иное)
    if os.getenv("ENV_TYPE", "dev") == "dev":
        logger.add(sys.stderr, level="DEBUG", format=dev_format, colorize=True)
        # logger.info("Режим разработки: логирование настроено для вывода в консоль.")

    # Конфигурация для продакшена
    else:
        # В консоль выводим только важные сообщения
        logger.add(sys.stderr, level="INFO", format=prod_format, colorize=False)
        
        # В файл пишем все, начиная с DEBUG, в формате JSON для машинного анализа
        logger.add(
            "logs/app.log",
            level="DEBUG",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            serialize=True,  # Структурированное логирование в JSON
        )
        # logger.info("Режим продакшена: логирование настроено для вывода в консоль и файл.")