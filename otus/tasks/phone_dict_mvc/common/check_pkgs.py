"""
Проверяет состояние third-party пакетов требующих импорта
"""
import subprocess
import sys

from exceptions import PhoneDictException

try:
    from loguru import logger # pip install loguru
except ModuleNotFoundError as e:
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", e.name])
        print(f"Библиотека {e.name} успешно установлена!")
        from loguru import logger
    except Exception as err:
        raise PhoneDictException(f"Произошла ошибка при установке: {err}")

try:
    import yaml # pip install pyyaml
except ModuleNotFoundError as e:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        logger.info(f"Библиотека {e.name} успешно установлена!")
        import yaml
    except Exception as err:
        raise PhoneDictException(f"Произошла ошибка при установке: {err}")
    

try:
    from prettytable import PrettyTable # pip install prettytable
except ModuleNotFoundError as e:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", e.name])
        logger.info(f"Библиотека {e.name} успешно установлена!")
        import yaml
    except Exception as err:
        raise PhoneDictException(f"Произошла ошибка при установке: {err}")