from ..contact import Contact
from .storage import Storage
from pathlib import Path

import re
from src.utils.loguru_config import AppLogger

logger = AppLogger().get_logger()

class PhoneDictionary:
    """Класс для представления сущности телефонного справочника"""
    json_data: dict
    storage: Storage
    is_json_data_changed: bool

    def __init__(self, storage: Storage):
        self.storage = storage
        self.load_data()

    def get_dict_folder(self):
        return self.storage.dicts_folder    
    
    def get_app_name(self):
        return self.storage.config.get_app_name()  
    
    def get_app_version(self):
        return self.storage.config.get_app_version()  

    def get_json_data(self) -> dict:
        return self.json_data

    def get_filename(self) -> str:
        return self.storage.get_json_file().name

    def get_current_dir(self) -> Path:
        return self.storage.get_current_dir()

    def get_contacts_list(self) -> list[Contact]:
        self.load_data()
        return self.json_data["contacts"]

    def is_data_changed(self) -> bool:
        """Проверка флага об изменениях данных справочника"""
        return self.is_json_data_changed

    def load_data(self, filename: str = ""):
        """Загрузка данных из файла в структуру класса"""
        json_data = self.storage.read_file(filename)
        if json_data:
            self.json_data = json_data
        else:
            self.json_data = {"contacts": []}
        self.set_is_json_data_changed(False)

    def save_data(self, filename: str = ""):
        """Сохранение данных из класса в файл"""
        self.storage.save_file(self.get_json_data(), filename)
        self.set_is_json_data_changed(False)

    def set_json_data(self, contact_list: list):
        """Обновление данных"""
        self.json_data["contacts"] = contact_list
        self.set_is_json_data_changed(True)

    def append_contact(self, contact: Contact):
        """Добавление контакта"""
        self.json_data["contacts"].append(contact.to_dict())
        self.set_is_json_data_changed(True)

    def delete_contact(self, contact: Contact):
        """Добавление контакта"""
        self.json_data["contacts"].remove(contact)
        self.set_is_json_data_changed(True)

    def get_contact(self, contact_id: str):
        return [contact for contact in self.json_data["contacts"] if contact["id"] == contact_id][0]

    def set_is_json_data_changed(self, is_json_data_changed: bool):
        """Установка флага изменения данных"""
        self.is_json_data_changed = is_json_data_changed
        if is_json_data_changed:
            self.save_data()

    @classmethod
    def _is_integer(cls, string) -> bool:
        if isinstance(string, int):
            return True
        pattern = r'^[-+]?\d+$'
        return bool(re.match(pattern, string))

    def get_next_id(self) -> str:
        result = 0
        contacts = self.get_contacts_list()
        if contacts:
            try:
                result = max([int(x.get("id", "0")) for x in contacts if self._is_integer(x.get("id", "0"))])
            except ValueError:
                return "1"
        return str(result + 1)