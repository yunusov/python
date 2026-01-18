from ..exceptions import ContactException
from ..common import CatchAllMeta
from ..model import Contact, PhoneDictionary, CONTACT_FIELDS
from .view_api import ViewApi
from prettytable import PrettyTable
from loguru import logger

import os
import sys


class View(metaclass=CatchAllMeta):
    """Класс для взаимодействия пользователя с программой"""

    pd: PhoneDictionary

    def __init__(self, pd: PhoneDictionary):
        self.pd = pd
        self.view_api = ViewApi(self.pd.get_current_dir() / self.pd.get_dict_folder())

    def clear_console(self):
        """Очистка консоли для отрисовки нового интерфейса"""
        if os.name == "nt":  # Windows
            _ = os.system("cls")
        else:  # Unix-like systems (Linux/MacOS)
            _ = os.system("clear")

    def open_file(self):
        """Меню открытия файла"""
        logger.info("open_file")
        dict_files = self.view_api.get_phone_dict_files()
        for key, file in dict_files.items():
            print(f"{key}. {file}")
        print("0 - выход в главное меню")
        cmd = input(
            "\nВыберите позицию файла в текущей директории который желаете открыть: "
        )

        logger.info(f"{cmd = }")
        if ("0" != cmd) and dict_files.get(cmd, None):
            filename = dict_files.get(cmd)
            logger.info(f"{filename = }")
            self.pd.load_data(filename)
            input(
                f"\n\nФайл {filename} открыт для работы. Нажмите <Enter> для продолжения"
            )

    def save_file(self):
        """Отображение меню сохранение файла с данными контактов"""
        logger.info("save_file")
        cmd = input(
            "Введите имя сохраняемого файла без расширения.\n"
            "Сохранить под тем же именем - <Enter>.\n"
            "Выход в главное меню - <0>: "
        )
        logger.info(f"{cmd = }")
        if cmd != "0":
            self.pd.save_data(cmd)

    def print_contact_table(self, contact_list: list = None):
        """Вывод таблицы с контактами"""
        contact_list = contact_list if contact_list else self.pd.get_contacts_list()
        table = PrettyTable(
            (
                str.upper(CONTACT_FIELDS[0]),
                str.upper(CONTACT_FIELDS[1]),
                str.upper(CONTACT_FIELDS[2]),
                str.upper(CONTACT_FIELDS[3]),
            )
        )

        for value in contact_list:
            contact = Contact(**value)
            table.add_row(contact.to_list())
        print(table)

    def show_all_contacts(self):
        """Меню отображения всех контактов в файле"""
        self.print_contact_table()
        input(f"\n\nВсе контакты из файла {self.pd.get_filename()}")

    def create_contact(self):
        """Меню создания контакта"""
        logger.info("create_contact")
        print("Создание контакта\n")
        id = self.pd.get_next_id()
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        comment = input("Введите комментарий: ")
        try:
            contact = Contact(id, name, phone, comment)
            self.pd.append_contact(contact)
            logger.info(f"Контакт {contact.to_dict()} создан!")
            input(f"\n\nКонтакт {contact.to_dict()} создан!")
        except ContactException as e:
            logger.error(e)
            input(f"\n\nКонтакт не создан по причине: '{e}'!")


    def find_contact(self):
        """Меню поиска контакта"""
        logger.info("find_contact")
        matched_contacts = list()
        cmd = input("Введите значение для поиска по полям: ")
        logger.info(f"{cmd = }")
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
        logger.info(f"{matched_contacts = }")
        input(f"\n\nПо вашему запросу найдено {len(matched_contacts)} стр.")

    def modify_contact(self):
        """Редактирование контакта"""
        logger.info("change_contact")
        contacts_list = self.pd.get_contacts_list()
        self.print_contact_table()
        cmd = input("\nВведите ID изменяемого контакта: ")
        logger.info(f"{cmd = }")
        if cmd:
            fixed_contact = ""
            for contact in contacts_list:
                if contact.get("id") == cmd:
                    contacts_list.remove(contact)
                    fixed_contact = contact
                    name = input("Введите имя: ")
                    phone = input("Введите номер телефона: ")
                    comment = input("Введите комментарий: ")
                    try:
                        contact = Contact(
                            cmd,
                            name,
                            phone if phone else contact.get("phone"),
                            comment if comment else contact.get("comment"),
                        )
                        contacts_list.append(contact.to_dict())
                        self.pd.set_json_data(contacts_list)
                        logger.info(f"{fixed_contact = } {contact.to_dict() = }")
                        input(f"\nКонтакт {contact.to_dict()} был обновлён!")
                    except ContactException as e:
                        logger.error(e)
                        input(f"\n\nКонтакт не изменён по причине: '{e}'!")    
                    break

    def delete_contact(self):
        """Запрос и удаление выбранного контакта"""
        self.print_contact_table()
        cmd = input("\nВведите ID удаляемого контакта: ")
        logger.info(f"{cmd = }")
        if cmd:
            contacts_list = self.pd.get_contacts_list()
            for contact in contacts_list:
                if contact.get("id") == cmd:
                    contacts_list.remove(contact)
                    self.pd.set_json_data(contacts_list)
                    logger.info(f"\nКонтакт {contact} был удалён!")
                    input(f"\nКонтакт {contact} был удалён!")
                    return
        input(f"\n\nКонтакт ID = {cmd} не обнаружен!")

    def exit_(self):
        """Выход из программы. Запрашивает сохранение файла при изменении данных."""
        if self.pd.is_data_changed():
            cmd = input(
                "\n\nДанные были изменены! Хотите перед выходом сохранить изменения? "
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
    MODIFY_CONTACT_TP = ("Изменить контакт", modify_contact)
    DELETE_CONTACT_TP = ("Удалить контакт", delete_contact)
    EXIT_TP = ("Выход из программы", exit_)

    MENU_METHOD_MAP = {
        "1": OPEN_FILE_TP,
        "2": SAVE_FILE_TP,
        "3": SHOW_ALL_CONTACTS_TP,
        "4": CREATE_CONTACT_TP,
        "5": FIND_CONTACT_TP,
        "6": MODIFY_CONTACT_TP,
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
