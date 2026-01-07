from loguru import logger


def setup_logging(current_dir = ""):
    """
    Настраивает логгер для всего приложения.
    """
    # Удаляем стандартный обработчик, чтобы избежать дублирования
    logger.remove()
    
    # В файл пишем все, начиная с DEBUG, в формате JSON для машинного анализа
    log_file = "logs/app.log"
    log_file = current_dir / log_file if current_dir else log_file

    logger.add(
        log_file,
        level="DEBUG",
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        serialize=False,  # Структурированное логирование в JSON
    )
    logger.info("Режим продакшена: логирование настроено для вывода в файл.")

if __name__ == "__main__":
    pass