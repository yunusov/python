from view import View


class Controller:
    con_view: View

    def __init__(self, con_view: View):
        self.con_view = con_view

    def run(self):
        while cmd := self.con_view.show_main_menu():
            self.con_view.exec_method(cmd)
