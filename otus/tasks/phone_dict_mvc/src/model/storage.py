from ..common.catch_all_meta import CatchAllMeta
from ..exceptions import PhoneDictException
from .config import Config

from loguru import logger
from pathlib import Path

import json


class Storage(metaclass=CatchAllMeta):
    """
    Класс для работы с файлом телефонного справочника
    """

    dicts_folder: str = "dicts"

    config: Config
    current_dir: Path
    json_file: Path

    def __init__(self, current_dir: Path, config: Config = None):
        """
        Аргументы:
        current_dir: текущая директория программы
        """
        if config:
            self.config = config
        else:
            self.config = Config(current_dir)
        self.current_dir = current_dir
        self.dicts_folder = self.config.get_storage_folder()
        self.json_file = current_dir / self.dicts_folder / self.config.get_storage_name()

    def get_current_dir(self) -> Path:
        return self.current_dir

    def get_json_file(self) -> Path:
        return self.json_file

    def set_json_file(self, json_file: Path):
        self.json_file = json_file
        self.config.set_storage_name(json_file.name)

    def read_file(self, filename: str) -> dict:
        """Чтение файла с диска. При необходимости создание и инициализация.

        Аргументы:
        filename: имя файла справочника.
        """
        json_file = self.get_json_file()
        if filename != json_file.name and filename:
            json_file = self.get_current_dir() / self.dicts_folder / filename
            self.set_json_file(json_file)
            self.config.write_config()
        result = {}
        if not self.json_file.exists():
            self.write_file({"contacts": []})
        with self.json_file.open(encoding="utf-8") as f:
            result = json.load(f)
        return result

    def save_file(self, json_data: dict, filename: str):
        """Сохранение файла с данными контактов

        Аргументы:
        filename: имя файла справочника.
        """
        json_file = self.get_json_file()
        if filename != json_file.name and filename:
            json_file = self.get_current_dir() / self.dicts_folder / (filename + ".json")
            self.set_json_file(json_file)
        self.write_file(json_data)

    def write_file(self, data):
        with self.json_file.open("w", encoding="utf-8") as f:
            json.dump(
                        data,
                        f,
                        ensure_ascii=False,
                        indent=4,
                        sort_keys=True,
                    )