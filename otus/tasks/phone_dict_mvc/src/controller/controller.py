from loguru import logger
from src.view import View


class Controller:
    """Класс-контроллер программы телефонный справочник"""
    con_view: View

    def __init__(self, con_view: View):
        self.con_view = con_view

    def run(self):
        try:
            while cmd := self.con_view.show_main_menu():
                self.con_view.exec_method(cmd)
        except KeyboardInterrupt as e:
            print("\n\nПользователь прекратил работу программы.")
        except Exception as e:
            print(f"\n\nИсключение '{e}' прервало работу программы. Обратитесь к разработчику.")
            logger.error(e)
        finally:
            exit()