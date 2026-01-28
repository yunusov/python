from pathlib import Path
import pytest
import random
import string

from src.model.config import Config
from src.model.phone_dict import PhoneDictionary
from src.model.storage import Storage
from src.view.view import View

RESOURCE_DIR = Path(__file__).parent.parent / "resources"
ALL_CHARS = string.ascii_letters + string.digits


@pytest.fixture
def view():
    return View(PhoneDictionary(Storage(RESOURCE_DIR, Config(RESOURCE_DIR))))


@pytest.fixture
def rand_string() -> str:
    """Генерирует случайную строку из букв и цифр."""
    result = random.choices(ALL_CHARS, k=8)
    return "".join(result)


@pytest.fixture
def rand_phone() -> str:
    """Генерирует случайную строку из цифр."""
    result = random.choices(string.digits, k=8)
    return "".join(result)