from pydantic import BaseModel

class Contact(BaseModel):
    """Класс для представления сущности контакт телефонного справочника"""

    id: str
    name: str
    phone: str
    comment: str
    owner: str


    def to_dict(self):
        """Метод для представления объекта в виде словаря"""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment,
            "owner": self.owner,
        }

    def to_list(self):
        """Метод для представления объекта в виде списка"""
        return [
            self.id,
            self.name,
            self.phone,
            self.comment,
            self.owner
        ]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_comment(self):
        return self.comment

