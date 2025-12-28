from view import Mvc_view


class Mvc_controller:
    con_view: Mvc_view

    def __init__(self, con_view: Mvc_view):
        self.con_view = con_view

    def run(self):
        while cmd := self.con_view.show_main_menu():
            self.con_view.exec_method(cmd)
