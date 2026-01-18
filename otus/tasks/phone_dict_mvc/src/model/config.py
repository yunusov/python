from src.common import CatchAllMeta
from src.exceptions import ConfigError
from loguru import logger
from pathlib import Path

import yaml


class Config(metaclass=CatchAllMeta):
    """Класс для работы с файлом конфигурации программы"""

    CONFIG_NAME: str = "config.yaml"

    config_file: dict
    current_dir: Path

    def __init__(self, current_dir: Path):
        self.current_dir = current_dir
        self.read_config()

    @classmethod
    def get_config_name(cls) -> str:
        return cls.CONFIG_NAME

    def get_storage_name(self) -> str:
        """Получение имени файла данных телефонного справочника"""
        try:
            return self.config_file["storage"]["name"]
        except KeyError as e:
            logger.error(e)
            raise ConfigError(
                "Конфигурационный файл повреждён. Обратитесь к разработчику."
            )

    def get_storage_folder(self) -> str:
        """Получение папки с файлом данных телефонного справочника"""
        try:
            return self.config_file["storage"]["folder"]
        except KeyError as e:
            logger.error(e)
            raise ConfigError(
                "Конфигурационный файл повреждён. Обратитесь к разработчику."
            )

    def set_storage_name(self, storage_name: str):
        """Запись имени файла данных телефонного справочника"""
        self.config_file["storage"]["name"] = storage_name

    def read_config(self):
        """Чтение из конфигурационного файла"""
        file = self.current_dir / Config.get_config_name()
        try:
            with open(file, "r", encoding="utf-8") as f:
                self.config_file = yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error(e)
            raise ConfigError(file=e.filename)

    def write_config(self):
        """Запись в конфигурационный файл"""
        file = self.current_dir / Config.get_config_name()
        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(self.config_file, f, sort_keys=False, allow_unicode=True)
