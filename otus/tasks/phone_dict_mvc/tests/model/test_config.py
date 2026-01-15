from pathlib import Path
from unittest.mock import patch

import pytest

from src.common.loguru_config import AppLogger
from src.exceptions import ConfigError


CURRENT_DIR = Path(__file__).parent.parent
RESOURCE_DIR = CURRENT_DIR / "resources"
logger = AppLogger(CURRENT_DIR).get_logger()

from src.model import Config


@pytest.fixture
def config():
    return Config(RESOURCE_DIR)


@pytest.fixture
def config_wrong():
    with patch("src.model.Config.get_config_name", return_value="config_wrong.yaml"):
        config_wrong = Config(RESOURCE_DIR)
    logger.info(f"{config_wrong.config_file = }")
    return config_wrong


def test_storage_name(config):
    assert type(config.get_storage_name()) == str


def test_storage_folder(config):
    assert type(config.get_storage_folder()) == str


def test_storage_folder_wrong(config_wrong):
    try:
        config_wrong.get_storage_folder()
        assert 1 == 2
    except Exception as e:
        logger.info(f"{e = }")
        assert type(e) == ConfigError


def test_open_notfound_file():
    try:
        Config(CURRENT_DIR / "foo")
        assert 1 == 2
    except Exception as e:
        logger.info(f"{e = }")
        assert type(e) == ConfigError
