# Scoring API

Сервис скоринга на стандартной библиотеке (`http.server`): клиент отправляет
POST-запрос с JSON на локейшн `/method`, сервис валидирует поля запроса,
аутентифицирует пользователя и возвращает результат метода.

Задание: [docs/task.md](docs/task.md).

## Структура

src/scoring_api/
├── api.py # HTTP-обработчик, описание полей (Field) и методов
├── scoring.py # расчёт скора и генерация интересов
└── main.py # точка входа CLI test/test_t.py # тесты

## Установка

```sh
uv sync
````

## Боевой запуск

```sh
uv run scoring-api            # порт по умолчанию — 8080
uv run scoring-api -p 9000 -l server.log
```

Либо модулем напрямую (в `api.py` есть блок `__main__`):

```sh
uv run python -m scoring_api.api -p 8080
```

Пример запроса:

```sh
curl -X POST -H "Content-Type: application/json" \
  -d '{"account": "horns&hoofs", "login": "h&f", "method": "online_score",
       "token": "<token>", "arguments": {"phone": "79175002040",
       "email": "stupnikov@otus.ru"}}' \
  http://127.0.0.1:8080/method/
```

## Запуск тестов

```sh
uv run pytest test -v
```

## Методы API

- `online_score` — аргументы `phone`, `email`, `first_name`, `last_name`, `birthday`, `gender`; ответ `{"score": <число>}`.
- `clients_interests` — аргументы `client_ids`, `date`; ответ `{"<id>": ["interest1", "interest2"], ...}`.
