import os
from loguru import logger

class CatchAllMeta(type):
    """
    Применяет декоратор loguru @logger.catch(reraise=True) ко всем методам наследующего класса класса.
    Кроме случая запуска pytest.
    """

    def __new__(cls, clsname, bases, dct):
        APP_ENV = os.environ.get("APP_ENV", "DEV")
        logger.info(f"{APP_ENV = } {clsname = }")
        new_dct = {}
        if APP_ENV == "PYTEST":
            new_dct = dct
        else:
            for attr_name, attr_value in dct.items():
                if callable(attr_value):
                    wrapped_attr = logger.catch(reraise=True)(attr_value)
                    new_dct[attr_name] = wrapped_attr
                else:
                    new_dct[attr_name] = attr_value
        return super().__new__(cls, clsname, bases, new_dct)
    