from common import CatchAllMeta
from model import Contact, PhoneDictionary, CONTACT_FIELDS
from prettytable import PrettyTable

import os
import sys


class View(metaclass=CatchAllMeta):
    """Класс для взаимодействия пользователя с программой"""
    pd: PhoneDictionary

    def __init__(self, pd: PhoneDictionary):
        self.pd = pd

    def clear_console(self):
        """Очистка консоли для отрисовки нового интерфейса"""
        if os.name == "nt":  # Windows
            _ = os.system("cls")
        else:  # Unix-like systems (Linux/MacOS)
            _ = os.system("clear")

    def open_file(self):
        """Меню открытия файла"""
        dict_files = {}
        i = 1
        current_dir = self.pd.get_current_dir() / self.pd.get_dict_folder()
        for file in current_dir.iterdir():
            if file.is_file() and file.name.lower().endswith(".json"):
                print(f"{i}. {file.name}")
                dict_files[str(i)] = file.name
                i += 1
        print("0 - выход в главное меню")
        cmd = input(
            "\nВыберите позицию файла в текущей директории который желаете открыть: "
        )

        if ("0" != cmd) and dict_files.__contains__(cmd):
            filename = dict_files.get(cmd)
            self.pd.load_data(filename)
            input(f"\n\nФайл {filename} открыт для работы. Нажмите <Enter> для продолжения")

    def save_file(self):
        """Отображение меню сохранение файла с данными контактов"""
        cmd = input(
            "Введите имя сохраняемого файла без расширения.\n"
            "Сохранить под тем же именем - <Enter>.\n"
            "Выход в главное меню - <0>: "
        )
        if cmd != "0":
            self.pd.save_data(cmd)

    def print_contact_table(self, contact_list: list = None):
        """Вывод таблицы с контактами"""
        contact_list = contact_list if contact_list else self.pd.get_contacts_list()
        table = PrettyTable((str.upper(CONTACT_FIELDS[0]),
                             str.upper(CONTACT_FIELDS[1]),
                             str.upper(CONTACT_FIELDS[2]),
                             str.upper(CONTACT_FIELDS[3])))

        for value in contact_list:
            contact = Contact(**value)
            table.add_row(contact.to_list())
        print(table)


    def show_all_contacts(self):
        """Меню отображения всех контактов в файле"""
        self.print_contact_table()
        input(f"\nВсе контакты из файла {self.pd.get_filename()}")

    def create_contact(self):
        """Меню создания контакта"""
        print("Создание контакта\n")
        not_correct_id_flag = True
        id = ""
        while not_correct_id_flag:
            id = input("Введите ID: ")
            if not id:
                print("Поле ID должно быть обязательно заполнено!")
                continue
            not_correct_id_flag = False
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        comment = input("Введите комментарий: ")
        contact = Contact(id, name, phone, comment)
        self.pd.append_contact(contact)
        input(f"Контакт {contact.to_dict()} создан!")

    def find_contact(self):
        """Меню поиска контакта"""
        matched_contacts = list()
        cmd = input("Введите значение для поиска по полям: ")
        if cmd:
            for contact in self.pd.get_contacts_list():
                if (
                    contact.get("id") == cmd
                    or cmd in contact.get("name")
                    or cmd in contact.get("phone")
                    or cmd in contact.get("comment")
                ):
                    matched_contacts.append(contact)
        self.print_contact_table(matched_contacts)
        input(f"\n\nПо вашему запросу найдено {len(matched_contacts)} стр.")

    def change_contact(self):
        """Редактирование контакта"""
        contacts_list = self.pd.get_contacts_list()
        self.print_contact_table()
        cmd = input("\nВведите ID изменяемого контакта: ")
        if cmd:
            fixed_contact = ""
            for contact in contacts_list:
                if contact.get("id") == cmd:
                    contacts_list.remove(contact)
                    fixed_contact = contact
                    name = input("Введите имя: ")
                    phone = input("Введите номер телефона: ")
                    comment = input("Введите комментарий: ")
                    contact = Contact(
                        cmd,
                        name if name else contact.get("name"),
                        phone if phone else contact.get("phone"),
                        comment if comment else contact.get("comment"),
                    )
                    contacts_list.append(contact.to_dict())
                    break

            if fixed_contact:
                self.pd.set_json_data(contacts_list)
                input(f"\nКонтакт {fixed_contact} был обновлён!")

    def delete_contact(self):
        """Запрос и удаление выбранного контакта"""
        self.print_contact_table()
        cmd = input("\nВведите ID удаляемого контакта: ")
        if cmd:
            contacts_list = self.pd.get_contacts_list()
            removed_contact = ""
            for contact in contacts_list:
                if contact.get("id") == cmd:
                    contacts_list.remove(contact)
                    removed_contact = contact
                    break
            if removed_contact:
                self.pd.set_json_data(contacts_list)
                input(f"\nКонтакт {removed_contact} был удалён!")

    def exit_(self):
        """Выход из программы. Запрашивает сохранение файла при изменении данных."""
        if self.pd.is_data_changed():
            cmd = input(
                "Данные были изменены! Хотите перед выходом сохранить изменения? "
                "(Y/N, Y - по умолчанию) "
            )
            if cmd.upper() == "Y" or not cmd:
                self.pd.save_data()
        print("Вы вышли из программы")
        sys.exit()

    OPEN_FILE_TP = ("Открыть файл", open_file)
    SAVE_FILE_TP = ("Сохранить файл", save_file)
    SHOW_ALL_CONTACTS_TP = ("Показать все контакты", show_all_contacts)
    CREATE_CONTACT_TP = ("Создать контакт", create_contact)
    FIND_CONTACT_TP = ("Найти контакт", find_contact)
    CHANGE_CONTACT_TP = ("Изменить контакт", change_contact)
    DELETE_CONTACT_TP = ("Удалить контакт", delete_contact)
    EXIT_TP = ("Выход из программы", exit_)

    MENU_METHOD_MAP = {
        "1": OPEN_FILE_TP,
        "2": SAVE_FILE_TP,
        "3": SHOW_ALL_CONTACTS_TP,
        "4": CREATE_CONTACT_TP,
        "5": FIND_CONTACT_TP,
        "6": CHANGE_CONTACT_TP,
        "7": DELETE_CONTACT_TP,
        "0": EXIT_TP,
    }

    def show_main_menu(self) -> str:
        """
        Вывод главного меню и считывание ввода с клавиатуры.
        Возвращает выбранную команду.
        """
        self.clear_console()
        print(f"Телефонный справочник {self.pd.get_filename()}\n\n")
        for key, value in self.MENU_METHOD_MAP.items():
            print(f"{key}. {value[0]}")

        cmd = input("\nВведите числовую команду: ")
        return cmd if cmd else "unknown"

    def exec_method(self, cmd: str):
        """Исполнение выбранного метода.

        Аргументы:
        cmd: введёная пользователем команда,
        """
        self.clear_console()
        if self.MENU_METHOD_MAP.__contains__(cmd):
            self.MENU_METHOD_MAP.get(cmd)[1](self)
        else:
            input("Ваша команда не распознана. Нажмите <Enter> и повторите ввод")
