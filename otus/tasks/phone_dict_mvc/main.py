from src.common.loguru_config import AppLogger
from src.controller import Controller
from src.model import PhoneDictionary, Storage, Config
from src.view import View

from pathlib import Path


def main():
    """Точка входа в программу."""
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    AppLogger(src_dir).get_logger()
    try:
        storage = Storage(src_dir, Config(current_dir))  
        phone_dict = PhoneDictionary(storage)
        con_view = View(phone_dict)
    except Exception as e:
        print(f"\n\nИсключение '{e}' прервало работу программы. "
              "Обратитесь к разработчику.")
        exit()

    controller = Controller(con_view)
    controller.run()


if __name__ == "__main__":
    main()
