import io
import os
import random
import string
from pathlib import Path
from unittest.mock import patch

import pytest

from src.model import Storage, PhoneDictionary, Config
from src.common import AppLogger

CURRENT_DIR = Path(__file__).parent.parent
RESOURCE_DIR = CURRENT_DIR / "resources"
DICTS_DIR = RESOURCE_DIR / "dicts"
logger = AppLogger(CURRENT_DIR).get_logger()
all_chars = string.ascii_letters + string.digits

from src.view import View


@pytest.fixture
def view():
    return View(PhoneDictionary(Storage(RESOURCE_DIR, Config(RESOURCE_DIR))))


@pytest.fixture
def rand_string() -> str:
    """Генерирует случайный строку заданной длины."""
    result = random.choices(all_chars, k=8)
    return "".join(result)


@pytest.fixture
def rand_phone() -> str:
    """Генерирует случайный строку заданной длины."""
    result = random.choices(string.digits, k=8)
    return "".join(result)


def get_last_output(capsys):
    captured = capsys.readouterr()
    output = captured.out.split("\n")
    return output[-1]


def test_open_file(view, monkeypatch, capsys):
    """Тестируем метод open_file для открытия случайного 1 из 4 предопределённых
    файлов справочников"""
    cmd = str(random.randint(1, 4))
    monkeypatch.setattr("sys.stdin", io.StringIO(cmd + "\n\n"))
    view.open_file()
    output = get_last_output(capsys)

    assert output == "Файл {}.json открыт для работы. Нажмите <Enter> для продолжения".format(
        cmd
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

    logger.info(f"{output = }")
    assert all(sub in output for sub in ["Контакт", "создан!", rand_string, rand_phone])


def test_find_contact(view, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем поиск пользователя"""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join([rand_string, rand_phone, rand_string, "\r", rand_string, "\r"])
        ),
    )
    view.create_contact()
    view.find_contact()
    output = get_last_output(capsys)
    logger.info(f"{output = }")

    assert output == "По вашему запросу найдено 1 стр."


def test_find_contact(view, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем поиск пользователя"""
    user_id = "".join([rand_string, rand_phone])
    modify_name = rand_string + "name"
    modify_phone = rand_phone + "phone"
    modify_comment = rand_string + "comment"
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join([rand_string, rand_phone, rand_string, "\r", user_id, 
                       modify_name, modify_phone, modify_comment , "\r"])
        ),
    )
    with patch("src.model.PhoneDictionary.get_next_id", return_value=user_id):
        view.create_contact()
        
    view.modify_contact()
    output = get_last_output(capsys)
    logger.info(f"{output = }")

    assert all(sub in output for sub in ["Контакт", "был обновлён!", modify_name,
                                         modify_phone, modify_comment])


def test_delete_contact(view, rand_string, rand_phone, monkeypatch, capsys):
    """Тестируем удаление пользователя"""
    user_id = "".join([rand_string, rand_phone])
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            "\n".join([rand_string, rand_phone, rand_string, "\r", user_id, "\r"])
        ),
    )
    with patch("src.model.PhoneDictionary.get_next_id", return_value=user_id):
        view.create_contact()
        
    view.delete_contact()
    output = get_last_output(capsys)
    logger.info(f"{output = }")

    assert all(sub in output for sub in ["Контакт", "был удалён!", rand_string,
                                         rand_phone, user_id])