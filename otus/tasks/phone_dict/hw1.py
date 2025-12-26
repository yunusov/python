from pathlib import Path
from typing import get_type_hints

import json
import os
import sys


CURRENT_DIR = Path(__file__).parent


class Contact:
    id: str
    name: str
    phone: str
    comment: str

    def __init__(self, id: str, name: str, phone: str, comment: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.comment = comment

    def to_dict(self):
        """Метод для представления объекта в виде словаря"""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment,
        }

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_comment(self):
        return self.comment
    

CONTACT_FIELDS = list(get_type_hints(Contact))


class PhoneDict:
    json_file: Path
    json_data: dict
    is_json_data_changed: bool

    def __init__(self, json_file: Path):
        self.json_file = json_file
        self.json_data = {"contacts": []}
        self.is_json_data_changed = False
        self.load_file(json_file)

    def load_file(self, json_file: Path):
        """Чтение файла с диска. При необходимости создание и инициализация.
        
        Аргументы:
        pd: экземпляр телефонного справочника.
        """
        if not json_file.exists():
            with json_file.open("w", encoding="utf-8") as f:
                json.dump(
                    self.get_json_data(),
                    f,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )
        with json_file.open(encoding="utf-8") as f:
             self.json_data = json.load(f)
        self.set_json_file(json_file)
        self.set_is_json_data_changed(False)

    def save_file(self, filename: str = ""):
        """Сохранение файла с данными контактов"""
        json_file = self.get_json_file()
        if filename != json_file.name and filename:
            json_file = CURRENT_DIR / (filename + ".json")
        with json_file.open("w", encoding="utf-8") as f:
            json.dump(
                self.get_json_data(),
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )
        self.set_json_file(json_file)
        self.set_is_json_data_changed(False)

    def get_json_file(self) -> Path:
        return self.json_file
    
    def get_json_data(self) -> dict:
        return self.json_data

    def get_contacts_list(self) -> list:
        return self.json_data["contacts"]

    def is_data_changed(self) -> bool:
        return self.is_json_data_changed

    def set_json_file(self, json_file: Path):
        self.json_file = json_file

    def set_json_data(self, json_data: dict):
        self.json_data["contacts"] = json_data
        self.set_is_json_data_changed(True)

    def append_contact(self, contact: Contact):
        self.json_data["contacts"].append(contact.to_dict())
        self.set_is_json_data_changed(True)

    def set_is_json_data_changed(self, is_json_data_changed: bool):
        self.is_json_data_changed = is_json_data_changed


def clear_console():
    """Очистка консоли для отрисовки нового интерфейса"""
    if os.name == "nt":  # Windows
        _ = os.system("cls")
    else:  # Unix-like systems (Linux/MacOS)
        _ = os.system("clear")


def open_file(pd: PhoneDict):
    """Меню открытия файла"""
    dict_files = {}
    i = 1
    for file in CURRENT_DIR.iterdir():
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
        pd.load_file(CURRENT_DIR / filename)
        input(f"Файл {filename} открыт для работы. Нажмите <Enter>")


def save_file(pd: PhoneDict):
    """Отображение меню сохранение файла с данными контактов"""
    cmd = input(
        "Введите имя сохраняемого файла без расширения.\n"
        "Сохранить под тем же именем - <Enter>.\nВыход в главное меню - <0>: "
    )
    if cmd != "0":
        pd.save_file(cmd)


def print_contact_table(contact_list: list):
    """Вывод таблицы с контактами"""
    print("------------------------------------------------------------")
    print(
        f"|{str.upper(CONTACT_FIELDS[0])}\t|{str.upper(CONTACT_FIELDS[1])}\t"
        f"|{str.upper(CONTACT_FIELDS[2])}\t|{str.upper(CONTACT_FIELDS[3])}"
    )
    print("------------------------------------------------------------")
    for value in contact_list:
        contact = Contact(**value)
        print(
            f"|{contact.get_id()}\t|{contact.get_name()}\t|{contact.get_phone()}\t|"
            f"{contact.get_comment()}"
        )
    print("------------------------------------------------------------")


def show_all_contacts(pd: PhoneDict):
    """Меню отображения всех контактов в файле"""
    print_contact_table(pd.get_contacts_list())
    input(f"\nВсе контакты из файла {pd.get_json_file()}")


def create_contact(pd: PhoneDict):
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
    pd.append_contact(contact)
    input(f"Контакт {contact.to_dict()} создан!")


def find_contact(pd: PhoneDict):
    """Меню поиска контакта"""
    matched_contacts = list()
    cmd = input("Введите значение для поиска по полям: ")
    if cmd:
        for contact in pd.get_contacts_list():
            if (
                contact.get("id") == cmd
                or cmd in contact.get("name")
                or cmd in contact.get("phone")
                or cmd in contact.get("comment")
            ):
                matched_contacts.append(contact)
    print_contact_table(matched_contacts)
    input(f"\n\nПо вашему запросу найдено {len(matched_contacts)} стр.")


def change_contact(pd: PhoneDict):
    """Редактирование контакта    

    Аргументы:
    pd: экземпляр телефонного справочника."""
    json_data = pd.get_contacts_list()
    print_contact_table(json_data)
    cmd = input("\nВведите ID изменяемого контакта: ")
    if cmd:
        fixed_contact = ""
        for contact in json_data:
            if contact.get("id") == cmd:
                json_data.remove(contact)
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
                json_data.append(contact.to_dict())
                break

        if fixed_contact:
            pd.set_json_data(json_data)
            input(f"\nКонтакт {fixed_contact} был обновлён!")


def delete_contact(pd: PhoneDict):
    """Запрос и удаление выбранного контакта
    
    Аргументы:
    pd: экземпляр телефонного справочника."""
    print_contact_table(pd.get_contacts_list())
    cmd = input("\nВведите ID удаляемого контакта: ")
    if cmd:
        contacts = pd.get_contacts_list()
        removed_contact = ""
        for contact in contacts:
            if contact.get("id") == cmd:
                contacts.remove(contact)
                removed_contact = contact
                break
        if removed_contact:
            pd.set_json_data(contacts)
            input(f"\nКонтакт {removed_contact} был удалён!")


def exit_(pd: PhoneDict):
    """Выход из программы. Запрашивает сохранение файла при изменении данных.
    
    Аргументы:
    pd: экземпляр телефонного справочника."""
    if pd.is_data_changed():
        cmd = input(
            "Данные были изменены! Хотите перед выходом сохранить изменения? "
            "(Y/N, Y - по умолчанию) "
        )
        if cmd.upper() == "Y" or not cmd:
            pd.save_file()
    print("Вы вышли из программы")
    sys.exit()


def show_main_menu(pd: PhoneDict) -> str:
    """
    Вывод главного меню и считывание ввода с клавиатуры.
    Возвращает выбранную команду.

    Аргументы:
    pd: кземпляр телефонного справочника.
    """
    clear_console()
    print(f"Телефонный справочник {pd.get_json_file()}\n\n")
    for key, value in MENU_METHOD_MAP.items():
        print(f"{key}. {value[0]}")

    cmd = input("\nВведите числовую команду: ")
    return cmd if cmd else "unknown"


def exec_method(cmd: str, pd: PhoneDict):
    """Исполнение выбранного метода.

    Аргументы:
    cmd: введёная пользователем команда,
    pd: экземпляр телефонного справочника.
    """
    clear_console()
    if MENU_METHOD_MAP.__contains__(cmd):
        MENU_METHOD_MAP.get(cmd)[1](pd)
    else:
        input("Ваша команда не распознана. Нажмите <Enter> и повторите ввод")


def main():
    """Точка входа в программу."""
    pd = PhoneDict(CURRENT_DIR / "phone_dict.json")
    while cmd := show_main_menu(pd):
        exec_method(cmd, pd)


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

if __name__ == "__main__":
    main()
