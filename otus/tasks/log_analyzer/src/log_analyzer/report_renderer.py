import os
import shutil
from pathlib import Path

import jinja2

from . import find_datalog, parse_file, prepare_json

extra_files = ["src/log_analyzer/static/jquery.min.js",
               "src/log_analyzer/static/jquery.tablesorter.min.js",]


def prepare_dict(data) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    while True:
        try:
            url, request_time = next(data)
            if result.get(url) is None:
                result[url] = [request_time]
            else:
                l = result[url]
                l.append(request_time)
                result[url] = l
        except StopIteration:
            break
    return result


def render_html(report_dir: str, max_fail_prc: int):
    file, file_date = find_datalog()

    output_path = Path(report_dir + f"/report_{file_date.strftime('%Y%m%d')}.html")
    if os.path.exists(output_path):
        return

    filedata = parse_file(file, max_fail_prc)
    dictdata = prepare_dict(filedata)
    items = prepare_json(dictdata)

    # 2. Загружаем шаблон из файла
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("src/log_analyzer/static"))
    template = env.get_template("report.html")

    # 3. Рендерим шаблон, передавая данные
    rendered_html = template.render(items=items)

    # 4. Сохраняем результат
    os.makedirs(report_dir, exist_ok=True)
    for file in extra_files:
        shutil.copy(
            os.path.join(file),
            os.path.join(report_dir),
        )
    output_path.write_text(rendered_html, encoding="utf-8")
