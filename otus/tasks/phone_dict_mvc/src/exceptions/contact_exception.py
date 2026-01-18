from .phone_dict_base_exception import PhoneDictBaseError


class ContactError(PhoneDictBaseError):
    """Общее исключение"""

    def __init__(self, message="Произошла ошибка при работе с контактом!"):
        self.message = message
        super().__init__(self.message)
