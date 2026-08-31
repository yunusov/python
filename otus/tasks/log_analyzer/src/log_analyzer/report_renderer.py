import datetime
import glob
import os
import re
from pathlib import Path

import jinja2

# Регулярное выражение для парсинга строки лога nginx.
# Якоримся на стабильной части: [time] "request" status bytes "referer" "ua" ... request_time.
# Такой подход не зависит от числа необязательных/пустых ведущих полей
# (remote_addr/remote_user/x_forwarded_for могут быть пустыми -> лишние пробелы).
LOG_LINE_RE = re.compile(
    r"\[(?P<time_local>[^\]]+)\] "
    r'"(?P<request>[^"]*)" '
    r"(?P<status>\d{3}) (?P<body_bytes_sent>\d+) "
    r'"(?P<http_referer>[^"]*)" '
    r'"(?P<http_user_agent>[^"]*)"'
    r"(?P<tail>.*) (?P<request_time>\d+\.\d+)\s*$"
)

# URL извлекается из поля request вида: "GET /api/v2/banner/25019354 HTTP/1.1"
URL_RE = re.compile(r"\S+\s+(?P<url>\S+)")


def find_datalog() -> tuple[str, datetime.datetime]:
    dir_path = "data"
    # Только файлы с расширением .gz
    # to-do: убрать glob
    gz_files = glob.glob(os.path.join(dir_path, "nginx-access-ui.log-????????.gz"))
    # Только файлы логов
    log_files = glob.glob(os.path.join(dir_path, "nginx-access-ui.log-????????"))
    result_file = ""
    result_date = datetime.datetime.strptime("19000101", "%Y%m%d").replace(
        tzinfo=datetime.UTC
    )
    for file in log_files:
        log_date = datetime.datetime.strptime(file[-8:], "%Y%m%d").replace(
            tzinfo=datetime.UTC
        )
        if (result_file is None) or (log_date > result_date):
            result_file = file
            result_date = log_date
    return (result_file, result_date)

def parse_file(file: str):
    """Генератор: читает лог и отдаёт пары (url, request_time) для корректных строк.

    Строки, которые не получилось разобрать (битые/не по формату), пропускаются.
    """
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            m = LOG_LINE_RE.search(line)
            if not m:
                continue
            url_m = URL_RE.search(m.group("request"))
            if not url_m:
                continue
            yield url_m.group("url"), float(m.group("request_time"))


def render_html(report_dir: str):
    file, file_date = find_datalog()
    m = parse_file(file)
    total_req = 0
    cnt_req = {}
    while True:
        try:
            url, request_time = next(m)
            if cnt_req.get(url, "") is None:
                cnt_req[url] = 1
            else:
                cnt_req[url] += 1   
            print(next(m))
        except StopIteration:
            break
    

    items = [
        {
            "URL": "1",
            "count": "coun2",
            "count_perc": "count_perc3",
            "time_sum": "time_sum4",
            "time_perc": "time_perc5",
            "time_avg": "time_avg6",
            "time_max": "time_max7",
            "time_med": "time_med8",
        },
        {
            "URL": "2",
            "count": "coun21",
            "count_perc": "count_perc32",
            "time_sum": "time_sum42",
            "time_perc": "time_perc52",
            "time_avg": "time_avg62",
            "time_max": "time_max72",
            "time_med": "time_med82",
        },
        {
            "URL": "3",
            "count": "coun23",
            "count_perc": "count_perc33",
            "time_sum": "time_sum43",
            "time_perc": "time_perc53",
            "time_avg": "time_avg63",
            "time_max": "time_max73",
            "time_med": "time_med83",
        },
    ]
    # 2. Загружаем шаблон из файла
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("src/log_analyzer/static"))
    template = env.get_template("report.html")

    # 3. Рендерим шаблон, передавая данные
    rendered_html = template.render(items=items)

    # 4. Сохраняем результат
    os.makedirs(report_dir, exist_ok=True)
    output_path = Path(report_dir + f"/report_{file_date.strftime('%Y%m%d')}.html")
    output_path.write_text(rendered_html, encoding="utf-8")
