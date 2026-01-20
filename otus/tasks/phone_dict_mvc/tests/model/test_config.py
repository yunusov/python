from pathlib import Path

from src.common.loguru_config import AppLogger
from src.exceptions import ConfigError
from src.model import Config


CURRENT_DIR = Path(__file__).parent.parent
logger = AppLogger(CURRENT_DIR).get_logger()


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
