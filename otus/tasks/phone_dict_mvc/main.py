from pathlib import Path
from controller import Controller
from model import Phone_dict, Storage
from view import View


def main():
    """Точка входа в программу."""
    storage = Storage(Path(__file__).parent)
    phone_dict = Phone_dict(storage)
    con_view = View(phone_dict)
    controller = Controller(con_view)
    controller.run()


if __name__ == "__main__":
    main()
