class PhoneDictException(Exception):
    """Общее исключение"""

    def __init__(self, message="Произошла ошибка"):
        self.message = message
        super().__init__(self.message)


class ConfigNotFoundException(Exception):
    """Исключение об отсутствии конфигурационного файла"""

    def __init__(self, file, message="Файл конфигурации программы {} не найден!"):
        self.message = message.format(file)
        super().__init__(self.message)


class ContactException(Exception):
    """Общее исключение"""

    def __init__(self, message="Произошла ошибка при работе с контактом!"):
        self.message = message
        super().__init__(self.message)