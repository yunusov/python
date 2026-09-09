import argparse
import json
from pathlib import Path

from structlog import get_logger

log = get_logger()

config = {
    "logfile": "",
    "log_dir": "LOG_DIR",
    "report_dir": "REPORT_DIR",
    "config_file": "src/log_analyzer/config.json",
    "max_fail_prc": 100,
    "report_size": 100,
}


def parse_args() -> dict:
    result = config.copy()

    parser = config_parser_args()
    args = parser.parse_args()
    config_json = read_config_json(
        args.config,
        result.get("config_file", ""),
    )
    result.update(config_json)

    # Переопределяем настройки
    args_logfile = args.logfile
    result["logfile"] = args_logfile or config_json.get("logfile") or result["logfile"]

    return result


def config_parser_args():
    parser = argparse.ArgumentParser(
        description="Анализатор логов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-l",
        "--logfile",
        default="",
        help="Файл с логами",
    )
    parser.add_argument(
        "--config",
        default="",
        help="Конфигурационный файл",
    )
    return parser


def read_config_json(args_config: str, default_config: str) -> dict:
    # Читаем JSON
    config_json = args_config if args_config else default_config
    try:
        data_path = Path(config_json)
        with data_path.open("r", encoding="utf-8") as f:
            config_items = json.load(f)
    except FileNotFoundError:
        log.error(f"Config file {config_json} not found!")
        raise
    return config_items
