class PhoneDictBaseError(Exception):
    """Общее исключение"""

    def __init__(self, message="Произошла ошибка"):
        self.message = message
        super().__init__(self.message)
