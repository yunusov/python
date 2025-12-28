from pathlib import Path
from controller import Mvc_controller
from model import Phone_dict, File_storage
from view import Mvc_view


def main():
    """Точка входа в программу."""
    storage = File_storage(Path(__file__).parent)
    phone_dict = Phone_dict(storage)
    con_view = Mvc_view(phone_dict)
    controller = Mvc_controller(con_view)
    controller.run()


if __name__ == "__main__":
    main()
