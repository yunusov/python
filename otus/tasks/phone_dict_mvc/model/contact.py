from typing import get_type_hints


class Contact:
    id: str
    name: str
    phone: str
    comment: str

    def __init__(self, id: str, name: str, phone: str, comment: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.comment = comment

    def to_dict(self):
        """Метод для представления объекта в виде словаря"""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment,
        }

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_comment(self):
        return self.comment
    

CONTACT_FIELDS = list(get_type_hints(Contact))