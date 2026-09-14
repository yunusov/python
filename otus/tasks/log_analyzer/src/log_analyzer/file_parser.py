import datetime
import gzip
import re
from collections.abc import Callable
from pathlib import Path
from statistics import median
from typing import Any

from structlog import get_logger
from tqdm import tqdm

from .log_file import LogFile

log = get_logger()

LOG_LINE_RE = re.compile(
    r"\[(?P<time_local>[^\]]+)\] "
    r'"(?P<request>[^"]*)" '
    r"(?P<status>\d{3}) (?P<body_bytes_sent>\d+) "
    r'"(?P<http_referer>[^"]*)" '
    r'"(?P<http_user_agent>[^"]*)"'
    r"(?P<tail>.*) (?P<request_time>\d+\.\d+)\s*$"
)

URL_RE = re.compile(r"\S+\s+(?P<url>/\S*)")

LOGFILE_RE = re.compile(r"nginx-access-ui\.log-(?P<date>\d{8})(?P<ext>\.gz)?$")


def find_datalog(dir_path: str) -> LogFile:
    directory = Path(dir_path)
    result_file = ""
    ext_file = ""
    result_date = datetime.datetime.strptime("19000101", "%Y%m%d").replace(
        tzinfo=datetime.UTC
    )
    try:
        for entry in directory.iterdir():
            if entry.is_file():
                m = LOGFILE_RE.fullmatch(entry.name)
                if not m:
                    continue
                str_date = m.group("date")
                log_date = datetime.datetime.strptime(str_date, "%Y%m%d").replace(
                    tzinfo=datetime.UTC
                )
                if (result_file is None) or (log_date > result_date):
                    result_file = entry.name
                    result_date = log_date
                    ext_file = m.group("ext")
    except FileNotFoundError as e:
        log.error(e)
        raise
    return LogFile(
        dir_path + "/" + result_file if result_file else None,
        result_date,
        ext_file,
    )


def parse_file(logfile: LogFile, max_fail_prc: int):
    """Генератор: читает лог и отдаёт пары (url, request_time) для корректных строк.

    Строки, которые не получилось разобрать (битые/не по формату), пропускаются.
    """
    cnt_fails = 0
    total_lines = 0
    if logfile.path is None:
        return
    path = Path(logfile.path)
    file_size = path.stat().st_size
    # open и gzip.open — перегруженные функции с разными наборами сигнатур:
    # без аннотации mypy выводит тип по первому присваиванию и падает на втором.
    fileopener: Callable[..., Any] = open
    if logfile.ext == ".gz":
        fileopener = gzip.open
        file_size *= 10
    with fileopener(logfile.path, "rt", encoding="utf-8") as f:
        pbar = tqdm(
            total=file_size, desc="Lines processed: ", unit="B", unit_scale=True
        )
        for line in f:
            pbar.update(len(line.encode("utf-8")))
            total_lines += 1
            m = LOG_LINE_RE.search(str(line))
            if not m:
                cnt_fails += 1
                continue
            url_m = URL_RE.search(m.group("request"))
            if not url_m:
                cnt_fails += 1
                continue

            yield url_m.group("url"), float(m.group("request_time"))
    pbar.close()
    if total_lines == 0:
        return
    fails_prc = 100 * cnt_fails / total_lines
    if fails_prc >= max_fail_prc:
        raise RuntimeError(
            "Достигнут максимальный уровень ошибочных записей! Скрипт остановлен."
        )


def prepare_json(data: dict) -> list[dict]:
    result: list[dict] = []
    total_count = sum(len(data[i]) for i in data)
    total_time_sum = sum(sum(data[i]) for i in data)
    for url, value in data.items():
        count = len(value)
        count_perc = round(100 * count / total_count, 3) if total_count != 0 else 0
        time_sum = round(sum(value), 3)
        time_perc = (
            round(100 * time_sum / total_time_sum, 3) if total_time_sum != 0 else 0
        )
        time_avg = round(time_sum / count, 3) if count != 0 else 0
        time_max = round(max(value), 3)
        time_med = round(median(value), 3)
        result.append(
            {
                "URL": url,
                "count": count,
                "count_perc": count_perc,
                "time_sum": time_sum,
                "time_perc": time_perc,
                "time_avg": time_avg,
                "time_max": time_max,
                "time_med": time_med,
            }
        )
    result.sort(key=lambda x: x["time_sum"], reverse=True)
    return result
