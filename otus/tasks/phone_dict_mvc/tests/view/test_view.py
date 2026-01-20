import io
import os
import random
import string
from pathlib import Path
from unittest.mock import patch

import pytest

from src.common import AppLogger
from src.model import Storage, PhoneDictionary, Config
from src.view import View


CURRENT_DIR = Path(__file__).parent.parent
RESOURCE_DIR = CURRENT_DIR / "resources"
DICTS_DIR = RESOURCE_DIR / "dicts"
logger = AppLogger(CURRENT_DIR).get_logger()
ALL_CHARS = string.ascii_letters + string.digits


@pytest.fixture
def view():
    return View(PhoneDictionary(Storage(RESOURCE_DIR, Config(RESOURCE_DIR))))


@pytest.fixture
def rand_string() -> str:
    """Генерирует случайный строку из букв и цифр."""
    result = random.choices(ALL_CHARS, k=8)
    return "".join(result)


@pytest.fixture
def rand_phone() -> str:
    """Генерирует случайный строку из цифр."""
    result = random.choices(string.digits, k=8)
    return "".join(result)


def get_last_output(capsys):
    """Выдаёт последнее сообщение из метода"""
    captured = capsys.readouterr()
    output = captured.out.split("\n")
    result = output[-1]
    logger.info(f"output = {result}")
    return result


def test_open_file(view, monkeypatch, capsys):
    """Тестируем метод open_file для открытия случайного 1 из 4 предопределённых
    файлов справочников"""
    cmd = str(random.randint(1, 4))
    monkeypatch.setattr("sys.stdin", io.StringIO(cmd + "\n\n"))
    view.open_file()
    output = get_last_output(capsys)

    assert (
        output
        == "Файл {}.json открыт для работы. Нажмите <Enter> для продолжения".format(cmd)
    )


def test_save_file(view, rand_string, monkeypatch):
    """Тестируем сохранение файла справочника со случайным именем"""
    monkeypatch.setattr("sys.stdin", io.StringIO(rand_string + "\n"))
    view.save_file()
    file_path = Path(DICTS_DIR / (rand_string + ".json"))

    assert file_path.exists()
    os.remove(file_path)


def test_create_contact(view, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем создание пользователя"""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO("\n".join([rand_string, rand_phone, rand_string, "\r"])),
    )
    view.create_contact()
    output = get_last_output(capsys)

    assert all(sub in output for sub in ["Контакт", "создан!", rand_string, rand_phone])


@pytest.mark.parametrize(
    "contact",
    [
        ("USER", "123", "comment"),
        ("U3#r", "ABC123", "   cOmmEnT  ! "),
        ("Юзер", "", ""),
        ("使用者", "XXII-0V-XVI", "非常に長い日本語解説" * 5),
    ],
)
def test_create_contact_params(view, contact, monkeypatch, capsys):
    """Тестируем параметризованное создание пользователя"""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO("\n".join([contact[0], contact[1], contact[2], "\r"])),
    )
    view.create_contact()
    output = get_last_output(capsys)

    assert all(
        sub in output
        for sub in ["Контакт", "создан!", contact[0], contact[1], contact[2]]
    )


def test_create_empty_name_contact(view, monkeypatch, capsys):
    """Тестируем создание 'пустого' контакта"""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO("\n".join(["", "", "", "\r", "name", "", "", "\r"])),
    )
    view.create_contact()
    output = get_last_output(capsys)

    assert (
        output == "Контакт не создан по причине: 'Имя контакта не должно быть пустое'!"
    )

    with patch("src.model.PhoneDictionary.get_next_id", return_value=None):
        view.create_contact()
    output = get_last_output(capsys)

    assert (
        output
        == "Контакт не создан по причине: 'Поле контакта ID не должно быть пустое'!"
    )


@pytest.mark.parametrize(
    "search_type",
    ["1", "2", "3"],
)
def test_find_contact(view, rand_string, rand_phone, search_type, monkeypatch, capsys):
    """Тестируем поиск контакта"""
    name_phone = rand_string + rand_phone
    if search_type == "1":
        search_str = rand_string
    elif search_type == "2":
        search_str = rand_phone
    else:
        search_str = name_phone[3:9]
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join(
                [
                    rand_string,
                    rand_phone,
                    name_phone,
                    "\r",
                    search_type,
                    search_str,
                    "\r",
                    search_type,
                    search_str + "rand",
                    "\r",
                ]
            )
        ),
    )
    view.create_contact()
    view.find_contact()
    output = get_last_output(capsys)

    assert output == "По вашему запросу найдено 1 стр."

    view.find_contact()
    output = get_last_output(capsys)

    assert output == "По вашему запросу найдено 0 стр."


def test_modify_contact(view, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем изменение контакта"""
    user_id = "".join([rand_string, rand_phone])
    modify_name = rand_string + "name"
    modify_phone = rand_phone + "phone"
    modify_comment = rand_string + "comment"
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join(
                [
                    rand_string,
                    rand_phone,
                    rand_string,
                    "\r",
                    user_id,
                    modify_name,
                    modify_phone,
                    modify_comment,
                    "\r",
                    user_id,
                    "",
                    modify_phone,
                    modify_comment,
                    "\r",
                ]
            )
        ),
    )
    with patch("src.model.PhoneDictionary.get_next_id", return_value=user_id):
        view.create_contact()

    view.modify_contact()
    output = get_last_output(capsys)

    assert all(
        sub in output
        for sub in [
            "Контакт",
            "был обновлён!",
            modify_name,
            modify_phone,
            modify_comment,
        ]
    )

    view.modify_contact()
    output = get_last_output(capsys)

    assert (
        output == "Контакт не изменён по причине: 'Имя контакта не должно быть пустое'!"
    )


def test_delete_contact(view, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем удаление пользователя"""
    user_id = "".join([rand_string, rand_phone])
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join(
                [
                    rand_string,
                    rand_phone,
                    rand_string,
                    "\r",
                    user_id,
                    "\r",
                    user_id,
                    "\r",
                ]
            )
        ),
    )
    with patch("src.model.PhoneDictionary.get_next_id", return_value=user_id):
        view.create_contact()

    view.delete_contact()
    output = get_last_output(capsys)

    assert all(
        sub in output
        for sub in ["Контакт", "был удалён!", rand_string, rand_phone, user_id]
    )

    view.delete_contact()
    output = get_last_output(capsys)

    assert output == "Контакт ID = {0} не обнаружен!".format(user_id)


@pytest.mark.parametrize(
    "cmd",
    ["Y", "\r", "N"],
)
def test_exit(view, cmd, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем выход из программы"""
    logger.info("test_exit")
    user_id = "".join([rand_string, rand_phone])
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join(
                [
                    rand_string,
                    rand_phone,
                    rand_string,
                    "\r",
                    cmd,
                    "3",
                    user_id,
                    "\r",
                    user_id,
                    "\r",
                ]
            )
        ),
    )
    with patch("src.model.PhoneDictionary.get_next_id", return_value=user_id):
        view.create_contact()
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        with patch("sys.exit", return_value=None):
            view.exit_()
        output = mock_stdout.getvalue()
        logger.info(f"{output = } {cmd = } {view.pd.get_filename() = }")
        assert "Вы вышли из программы" in output

    if cmd != "N":
        view.find_contact()
        logger.info(f"{view.pd.get_filename() = }")
        output = get_last_output(capsys)

        assert output == "По вашему запросу найдено 1 стр."
        view.delete_contact()

        output = get_last_output(capsys)

        assert all(
            sub in output
            for sub in ["Контакт", "был удалён!", rand_string, rand_phone, user_id]
        )
        view.pd.save_data()
