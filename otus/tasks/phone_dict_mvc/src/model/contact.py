from typing import get_type_hints
from ..exceptions import ContactError


class Contact:
    """Класс для представления сущности контакт телефонного справочника"""

    id: str
    name: str
    phone: str
    comment: str

    def _validate(self):
        if not self.id:
            raise ContactError("Поле контакта ID не должно быть пустое")
        if not self.name:
            raise ContactError("Имя контакта не должно быть пустое")

    def __init__(self, id: str, name: str, phone: str, comment: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.comment = comment
        self._validate()

    def to_dict(self):
        """Метод для представления объекта в виде словаря"""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment,
        }

    def to_list(self):
        """Метод для представления объекта в виде списка"""
        return [
            self.id,
            self.name,
            self.phone,
            self.comment,
        ]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_comment(self):
        return self.comment


CONTACT_FIELDS = list(get_type_hints(Contact))
