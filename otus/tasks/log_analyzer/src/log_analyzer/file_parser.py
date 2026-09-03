import datetime
import gzip
import re
from pathlib import Path
from statistics import median

LOG_LINE_RE = re.compile(
    r"\[(?P<time_local>[^\]]+)\] "
    r'"(?P<request>[^"]*)" '
    r"(?P<status>\d{3}) (?P<body_bytes_sent>\d+) "
    r'"(?P<http_referer>[^"]*)" '
    r'"(?P<http_user_agent>[^"]*)"'
    r"(?P<tail>.*) (?P<request_time>\d+\.\d+)\s*$"
)

URL_RE = re.compile(r"\S+\s+(?P<url>\S+)")

LOGFILE_RE = re.compile(r"nginx-access-ui.log-(?P<date>\d{8})(?P<ext>.gz)?")


def find_datalog(dir_path: str) -> tuple[str | None, datetime.datetime]:
    # Только файлы с расширением .gz
    # to-do: убрать glob
    directory = Path(dir_path)
    result_file = ""
    result_date = datetime.datetime.strptime("19000101", "%Y%m%d").replace(
        tzinfo=datetime.UTC
    )
    for entry in directory.iterdir():
        if entry.is_file():
            m = LOGFILE_RE.search(entry.name)
            if not m:
                continue
            str_date = m.group("date")
            log_date = datetime.datetime.strptime(str_date, "%Y%m%d").replace(
                tzinfo=datetime.UTC
            )
            if (result_file is None) or (log_date > result_date):
                result_file = entry.name
                result_date = log_date
    return (dir_path + "/" + result_file if result_file else None, result_date)


def parse_file(file: str, max_fail_prc: int):
    """Генератор: читает лог и отдаёт пары (url, request_time) для корректных строк.

    Строки, которые не получилось разобрать (битые/не по формату), пропускаются.
    """
    total_lines = count_lines(file)
    cnt_fails = 0
    print(f"parse_file {file = }")
    fileopener = gzip.open if file[-3:] == ".gz" else open
    with fileopener(file, "rt", encoding="utf-8") as f:
        for line in f:
            print(f"{line = }")

            m = LOG_LINE_RE.search(str(line))
            if not m:
                cnt_fails += 1
                continue
            url_m = URL_RE.search(m.group("request"))
            if not url_m:
                cnt_fails += 1
                continue

            yield url_m.group("url"), float(m.group("request_time"))
    fails_prc = 100 * cnt_fails / total_lines
    if fails_prc >= max_fail_prc:
        raise RuntimeError(
            "Достигнут максимальный уровень ошибочных записей! Скрипт остановлен."
        )


def count_lines(filename):
    result = 0
    fileopener = gzip.open if filename[-3:] == ".gz" else open
    with fileopener(filename, "r") as f:
        result = sum(1 for line in f)
    print(f"count_lines {result = }")
    return result


def prepare_json(data: dict) -> list[dict]:
    result: list[dict] = []
    total_count = sum([len(data[i]) for i in data])
    total_time_sum = sum([sum(data[i]) for i in data])
    for url, value in data.items():
        count = len(value)
        count_perc = round(100 * count / total_count, 2)
        time_sum = round(sum(value), 2)
        time_perc = round(100 * time_sum / total_time_sum, 2)
        time_avg = round(time_sum / count, 2)
        time_max = round(max(value), 2)
        time_med = round(median(value), 2)
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
    return result
