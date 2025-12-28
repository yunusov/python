from .storage import File_storage
from .contact import Contact
from pathlib import Path

class Phone_dict:
    json_data: dict
    storage: File_storage
    is_json_data_changed: bool

    def __init__(self, storage: File_storage):
        self.storage = storage
        self.load_data()
        self.set_is_json_data_changed(False)

    def get_json_data(self) -> dict:
        return self.json_data

    def get_filename(self) -> str:
        return self.storage.get_json_file().name
    
    def get_current_dir(self) -> Path:
        return self.storage.get_current_dir()

    def get_contacts_list(self) -> list:
        return self.json_data["contacts"]

    def is_data_changed(self) -> bool:
        return self.is_json_data_changed

    def load_data(self, filename: str = ""):
        json_data = self.storage.read_file(filename)
        if json_data:
            self.json_data = json_data
        else:
            self.json_data = {"contacts": []}
        self.set_is_json_data_changed(False)

    def save_data(self, filename: str = ""):
        self.storage.save_file(self.get_json_data(), filename)
        self.set_is_json_data_changed(False)

    def set_json_data(self, contact_list: list):
        self.json_data["contacts"] = contact_list
        self.set_is_json_data_changed(True)

    def append_contact(self, contact: Contact):
        self.json_data["contacts"].append(contact.to_dict())
        self.set_is_json_data_changed(True)

    def set_is_json_data_changed(self, is_json_data_changed: bool):
        self.is_json_data_changed = is_json_data_changed
