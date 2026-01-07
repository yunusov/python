class PhoneDictException(Exception):
    """Общее исключение"""
    def __init__(self, message="Произошла ошибка"):
        self.message = message
        super().__init__(self.message)

class ConfigNotFoundException(Exception):
    """Исключение об отсутствии конфигурационного файла"""
    def __init__(self, message=f"Файл конфигурации программы config.yaml не найден!"):
        self.message = message
        super().__init__(self.message)