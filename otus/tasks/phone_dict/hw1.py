from pathlib import Path
from typing import get_type_hints

import json
import os
import sys


CURRENT_DIR = Path(__file__).parent
json_file = CURRENT_DIR / "phone_dict.json"
json_data = dict()
is_json_data_changed = False


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


USER_FIELDS = list(get_type_hints(Contact))


def clear_console():
    if os.name == "nt":  # Windows
        _ = os.system("cls")
    else:  # Unix-like systems (Linux/MacOS)
        _ = os.system("clear")


def wrong_input():
    input("Ваша команда не распознана. Нажмите <Enter> и повторите ввод")


def open_file():
    global json_file
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
        json_file = CURRENT_DIR / filename
        load_file()
        input(f"Файл {filename} открыт для работы. Нажмите <Enter>")


def save_json_data(filename: str):
    global json_file
    if filename != json_file.name and filename:
        json_file = CURRENT_DIR / (filename + ".json")
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(
            json_data,
            f,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
        )


def save_file():
    global is_json_data_changed
    cmd = input(
        "Введите имя сохраняемого файла без расширения.\n"
        "Сохранить под тем же именем - <Enter>.\nВыход в главное меню - <0>: "
    )
    if cmd != "0":
        save_json_data(cmd)
        is_json_data_changed = False


def print_contact_table(contact_list: list):
    print("------------------------------------------------------------")
    print(
        f"|{str.upper(USER_FIELDS[0])}\t|{str.upper(USER_FIELDS[1])}\t"
        f"|{str.upper(USER_FIELDS[2])}\t|{str.upper(USER_FIELDS[3])}"
    )
    print("------------------------------------------------------------")
    for value in contact_list:
        user = Contact(**value)
        print(
            f"|{user.get_id()}\t|{user.get_name()}\t|{user.get_phone()}\t|"
            f"{user.get_comment()}"
        )
    print("------------------------------------------------------------")


def show_all_contacts():
    print_contact_table(json_data["users"])
    input(f"\nВсе контакты из файла {json_file}")


def create_contact():
    global json_data, is_json_data_changed
    print("Создание контакта\n")
    not_correct_id_flag = True
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
    json_data["users"].append(contact.to_dict())
    is_json_data_changed = True
    input(f"Контакт {contact.to_dict()} создан!")


def find_contact():
    matched_contacts = list()
    cmd = input("Введите значение для поиска по полям: ")
    if cmd:
        for user in json_data["users"]:
            if (
                user.get("id") == cmd
                or cmd in user.get("name")
                or cmd in user.get("phone")
                or cmd in user.get("comment")
            ):
                matched_contacts.append(user)
    print_contact_table(matched_contacts)
    input(f"\n\nПо вашему запросу найдено {len(matched_contacts)} стр.")


def change_contact():
    global is_json_data_changed
    print_contact_table(json_data["users"])
    cmd = input("\nВведите ID изменяемого контакта: ")
    if cmd:
        users = json_data["users"]
        fixed_user = ""
        for user in users:
            if user.get("id") == cmd:
                users.remove(user)
                fixed_user = user
                name = input("Введите имя: ")
                phone = input("Введите номер телефона: ")
                comment = input("Введите комментарий: ")
                contact = Contact(
                    cmd,
                    name if name else user.get("name"),
                    phone if phone else user.get("phone"),
                    comment if comment else user.get("comment"),
                )
                json_data["users"].append(contact.to_dict())
                break

        if fixed_user:
            json_data["users"] = users
            input(f"\n Контакт {fixed_user} был обновлён!")
            is_json_data_changed = True


def delete_contact():
    global is_json_data_changed
    print_contact_table()
    cmd = input("\nВведите ID удаляемого контакта: ")
    if cmd:
        users = json_data["users"]
        removed_user = ""
        for user in users:
            if user.get("id") == cmd:
                users.remove(user)
                removed_user = user
                break
        if removed_user:
            json_data["users"] = users
            input(f"\n Контакт {removed_user} был удалён!")
            is_json_data_changed = True


def exit_():
    if is_json_data_changed:
        cmd = input(
            "Данные были изменены! Хотите перед выходом сохранить изменения? "
            "(Y/N, Y - по умолчанию) "
        )
        if cmd.upper() == "Y" or not cmd:
            save_json_data(json_file.name)
    print("Вы вышли из программы")
    sys.exit()


def show_main_menu() -> str:
    """Показывает меню и считывает ввод с клавиатуры"""
    clear_console()
    print(f"Телефонный справочник {json_file}\n\n")
    for key, value in menu_method_map.items():
        print(f"{key}. {value[0]}")

    cmd = input("\nВведите числовую команду: ")
    return cmd if cmd else "unknown"


def exec_method(cmd: str):
    """Запускает выбранный метод"""
    clear_console()
    if menu_method_map.__contains__(cmd):
        menu_method_map.get(cmd)[1]()
    else:
        wrong_input()


def load_file():
    global json_data, is_json_data_changed
    if not json_file.exists():
        with json_file.open("w", encoding="utf-8") as f:
            json.dump(
                {"users": []},
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )
    with json_file.open(encoding="utf-8") as f:
        json_data = json.load(f)
    is_json_data_changed = False


def main():
    load_file()
    while cmd := show_main_menu():
        exec_method(cmd)


open_file_tp = ("Открыть файл", open_file)
save_file_tp = ("Сохранить файл", save_file)
show_all_contacts_tp = ("Показать все контакты", show_all_contacts)
create_contact_tp = ("Создать контакт", create_contact)
find_contact_tp = ("Найти контакт", find_contact)
change_contact_tp = ("Изменить контакт", change_contact)
delete_contact_tp = ("Удалить контакт", delete_contact)
exit_tp = ("Выход из программы", exit_)

menu_method_map = {
    "1": open_file_tp,
    "2": save_file_tp,
    "3": show_all_contacts_tp,
    "4": create_contact_tp,
    "5": find_contact_tp,
    "6": change_contact_tp,
    "7": delete_contact_tp,
    "0": exit_tp,
}

if __name__ == "__main__":
    main()
