from .phone_dict_base_exception import PhoneDictBaseError


class ConfigError(PhoneDictBaseError):
    """Исключение конфигурационного файла"""

    def __init__(self, file, message="Файл конфигурации программы {} не найден!"):
        self.message = message.format(file)
        super().__init__(self.message)
