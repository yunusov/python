import sys

from loguru import logger


class AppLogger:
    _instance = None
    _current_dir = None

    def __new__(cls, current_dir=None):
        cls._current_dir = current_dir
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self):
        """
        Настраивает логгер для всего приложения.
        """
        # Удаляем стандартный обработчик, чтобы избежать дублирования
        logger.remove()

        logger.add(
            sys.stderr,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
        )
        # В файл пишем все, начиная с DEBUG
        log_file = "logs/app.log"
        log_file = self._current_dir / log_file if self._current_dir else log_file

        logger.add(
            log_file,
            level="DEBUG",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            serialize=False,
        )
        # logger.info("Режим продакшена: логирование настроено для вывода в файл.")

    def get_logger(self):
        return logger

    def flush_logs(self, signum, frame):
        logger.warning(f"Получен сигнал SIGINT или SIGKILL ({signum})")
        logger.remove()  # Сбросит буферы и закроет файлы
        self.kill_now = True
