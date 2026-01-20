from pathlib import Path


class ViewApi:
    """API для работы с классом View"""

    @staticmethod
    def get_phone_dict_files(dict_folder: Path) -> dict:
        """Получаем dict файлов телефонного справочника
        
        Аргументы:
        dict_folder: папка в которой хранятся справочники с данными"""
        result = {}
        i = 1
        for file in dict_folder.iterdir():
            if file.is_file() and file.name.lower().endswith(".json"):
                result[str(i)] = file.name
                i += 1
        return result

    @staticmethod
    def get_matched_contacts(search_type: str, cmd: str, contacts: list) -> list:
        """Формирование списка найденных контактов на основе типа поиска и введённого значения
        
        Аргументы:
        search_type: тип поиска. 1 - по имени, 2 - по номеру телефона, 3 - по всем полям
        cmd: значение для поиска
        contact_list: список контактов справочника
        """
        result = []
        for contact in contacts:
            if ((search_type == "1"
                    and cmd == contact.get("name"))
                or (search_type == "2"
                    and cmd == contact.get("phone")) 
                or (search_type == "3"
                    and (contact.get("id") == cmd
                        or cmd in contact.get("name")
                        or cmd in contact.get("phone")
                        or cmd in contact.get("comment")))
            ):
                result.append(contact)
        return result