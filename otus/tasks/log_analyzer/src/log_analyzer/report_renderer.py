import json
import os
import shutil
from pathlib import Path
from string import Template

from .file_parser import find_datalog, parse_file, prepare_json

TOP_FOLDER = Path(__file__).resolve().parent.parent.parent
PARENT_FOLDER = Path(__file__).resolve().parent

extra_files = [
    "static/jquery.min.js",
    "static/jquery.tablesorter.min.js",
]


def prepare_dict(data) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for url, request_time in data:
        result.setdefault(url, []).append(request_time)
    return result


def render_html(cfg: dict):
    report_dir = cfg.get("report_dir", "")
    log_dir = cfg.get("log_dir", "")
    max_fail_prc = cfg.get("max_fail_prc", 100)
    report_size = cfg.get("report_size", 100)
    force = cfg.get("force", False)

    logfile = find_datalog(log_dir)
    if logfile.path is None:
        return

    output_path = (
        TOP_FOLDER / report_dir / f"report-{logfile.date.strftime('%Y.%m.%d')}.html"
    )
    if os.path.exists(output_path) and not force:
        return

    filedata = parse_file(logfile, max_fail_prc)
    dictdata = prepare_dict(filedata)
    items = prepare_json(dictdata)

    items = items[:report_size]
    # 2. Загружаем шаблон из файла
    with open(PARENT_FOLDER / "static/report.html", encoding="utf-8") as f:
        template = Template(f.read())

    # 3. Рендерим: подставляем только $table_json
    table_json = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    rendered_html = template.safe_substitute(table_json=table_json)

    # 4. Сохраняем результат
    os.makedirs(TOP_FOLDER / report_dir / "static", exist_ok=True)
    for file in extra_files:
        shutil.copy(
            PARENT_FOLDER / file,
            TOP_FOLDER / report_dir / "static",
        )
    output_path.write_text(rendered_html, encoding="utf-8")
