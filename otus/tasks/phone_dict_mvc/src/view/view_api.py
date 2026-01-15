from pathlib import Path


class ViewApi:
    """API для работы с классом View"""

    def __init__(self, dict_folder: Path):
        self.dict_folder = dict_folder

    def get_dict_folder(self) -> Path:
        return self.dict_folder

    def get_phone_dict_files(self) -> dict:
        """Получаем dict файлов телефонного справочника"""
        result = {}
        i = 1
        for file in self.get_dict_folder().iterdir():
            if file.is_file() and file.name.lower().endswith(".json"):
                result[str(i)] = file.name
                i += 1
        return result
