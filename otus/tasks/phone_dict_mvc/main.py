import common.check_pkgs  # Не удалять! Проверка состояния пакетов.

from common.loguru_config import setup_logging
from controller import Controller
from model import PhoneDictionary, Storage
from pathlib import Path
from view import View


def main():
    """Точка входа в программу."""
    current_dir = Path(__file__).parent
    setup_logging(current_dir)
    try:
        storage = Storage(current_dir)  
        phone_dict = PhoneDictionary(storage)
        con_view = View(phone_dict)
    except Exception as e:
        print(f"\n\nИсключение '{e.message}' прервало работу программы. Обратитесь к разработчику.")
        exit()

    controller = Controller(con_view)
    controller.run()


if __name__ == "__main__":
    main()
