from .contact import Contact
from .storage import Storage
from pathlib import Path


class PhoneDictionary:
    """Класс для представления сущности телефонного справочника"""
    json_data: dict
    storage: Storage
    is_json_data_changed: bool

    def __init__(self, storage: Storage):
        self.storage = storage
        self.load_data()

    def get_dict_folder(self):
        return Storage.dicts_folder    

    def get_json_data(self) -> dict:
        return self.json_data

    def get_filename(self) -> str:
        return self.storage.get_json_file().name

    def get_current_dir(self) -> Path:
        return self.storage.get_current_dir()

    def get_contacts_list(self) -> list:
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

    def set_is_json_data_changed(self, is_json_data_changed: bool):
        """Установка флага изменения данных"""
        self.is_json_data_changed = is_json_data_changed
