from pathlib import Path
import pytest

from src.model.config import Config


RESOURCE_DIR = Path(__file__).parent.parent / "resources"


@pytest.fixture
def config():
    return Config(RESOURCE_DIR)


@pytest.fixture
def config_wrong(mocker):
    mocker.patch("src.model.Config.get_config_name", return_value="config_wrong.yaml")
    config_wrong = Config(RESOURCE_DIR)
    return config_wrong