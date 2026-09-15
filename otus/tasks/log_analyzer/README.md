# log_analyzer

Консольная утилита анализа access-логов nginx: находит самый свежий лог, собирает статистику по URL и строит HTML-отчёт с таблицей самых «дорогих» по суммарному времени запросов адресов.

## Как это работает

1. **Поиск лога** — в `log_dir` выбирается файл с **максимальной датой в имени** по шаблону
   `nginx-access-ui.log-YYYYMMDD` (опционально `.gz`). Файлы с другими расширениями (`.bz2`, `.bak`, …) игнорируются. Логов нет — это не ошибка: утилита просто завершится.
2. **Парсинг** — генератор построчно разбирает записи регуляркой и отдаёт пары `(url, request_time)`. Если доля некорректных строк превысила `max_fail_prc` (в %) — работа завершается ошибкой.
3. **Агрегация** — по каждому URL считаются: `count`, `count_perc`, `time_sum`, `time_perc`, `time_avg`, `time_max`, `time_med`.
4. **Отчёт** — топ-`report_size` URL, отсортированных по `time_sum` (по убыванию), сериализуется в JSON и подставляется в HTML-шаблон (`string.Template.safe_substitute` по `$table_json`); таблица сортируется на клиенте jQuery tablesorter.
5. Результат: `report_dir/report-YYYY.MM.DD.html` (дата — из имени лога) + `static/` с js-библиотеками. Если отчёт уже существует и `force=false` — перегенерация не выполняется.

## Требования

- Python **3.11+** и [Poetry](https://python-poetry.org/) **2.x**
- либо только Docker (см. ниже)

## Установка и запуск

```bash
poetry install                       # зависимости + сам пакет (editable)
poetry run main-run                  # запуск с конфигом по умолчанию
poetry run main-run --config path/to/config.json   # со своим конфигом
poetry run main-run --config ... --logfile ""      # логирование в консоль
```

Windows-ярлык (`start.bat` → `make -f docs/Makefile run`):

```bat
start.bat
```

## Конфигурация

Конфиг — JSON. Значения из файла накладываются на встроенные дефолты
(`src/log_analyzer/config.json`); ключ `logfile` можно переопределить ключом CLI `--logfile`.

| Ключ | По умолчанию | Описание |
|---|---|---|
| `logfile` | `""` | имя файла лога в `logs/`; пусто — вывод в stderr (JSON-режим structlog при записи в файл) |
| `log_dir` | `LOG_DIR` | директория с входными логами (относительно CWD или абсолютный путь) |
| `report_dir` | `REPORT_DIR` | директория для отчётов (относительно корня проекта или абсолютный путь) |
| `max_fail_prc` | `100` | максимально допустимая доля битых строк, % |
| `report_size` | `500` | сколько URL попадает в отчёт (топ по `time_sum`) |
| `force` | `false` | `true` — перегенерировать отчёт, даже если он уже существует |

Пример своего конфига:

```json
{
    "logfile": "",
    "log_dir": "/data/logs",
    "report_dir": "/data/reports",
    "max_fail_prc": 100,
    "report_size": 500,
    "force": true
}
```

## Docker

Входные данные (логи, конфиг) и выход (отчёт) подключаются volume-ами:

```bash
# сборка
docker build -t log-analyzer .

# логи -> read-only, отчёт -> в текущую REPORT_DIR (PowerShell)
docker run --rm `
  -v "${PWD}\LOG_DIR:/data/logs:ro" `
  -v "${PWD}\REPORT_DIR:/data/reports" `
  log-analyzer

# со своим конфигом
docker run --rm `
  -v "${PWD}\LOG_DIR:/data/logs:ro" `
  -v "${PWD}\REPORT_DIR:/data/reports" `
  -v "${PWD}\my-config.json:/config/config.json:ro" `
  log-analyzer --config /config/config.json
```

Тот же сценарий через `docker-compose.yml`:

```bash
docker compose up --build
```

## Разработка

```bash
make -f docs/Makefile run          # запуск
make -f docs/Makefile linting      # ruff format + ruff check --fix
make -f docs/Makefile tests        # pytest -xvvs
make -f docs/Makefile test-cov     # pytest с coverage-отчётом

poetry run pytest test -q          # тесты (поиск лога, парсер, метрики, рендер, конфиг)
poetry run ruff check src test     # линтер
poetry run black --check src test  # формат
poetry run isort --check-only src test
poetry run mypy src/log_analyzer test
poetry run pre-commit run --all-files   # все хуки разом
```

CI (GitHub Actions, `.github/workflows/ci.yml`) прогоняет на каждом push/PR: ruff, black, isort, mypy и тесты.

## Структура проекта

```
log_analyzer/
├── Dockerfile, docker-compose.yml, config-docker.json   # контейнер
├── docs/                    # Makefile, текст задания
├── LOG_DIR/                 # входные nginx-логи (в git не хранятся)
├── REPORT_DIR/              # сгенерированные отчёты (в git не хранятся)
├── src/log_analyzer/
│   ├── main.py              # точка входа (entry point main-run)
│   ├── arg_parser.py        # CLI + слияние конфигов
│   ├── file_parser.py       # поиск лога, генератор-парсер, метрики
│   ├── log_file.py          # LogFile (dataclass)
│   ├── report_renderer.py   # сборка и запись HTML-отчёта
│   ├── log_setup.py         # structlog + ротация логов
│   ├── config.json          # конфиг по умолчанию
│   └── static/              # report.html + jquery
└── test/                    # pytest-тесты
```
