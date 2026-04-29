"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД



Описание/Пошаговая инструкция выполнения домашнего задания:
создайте docker-compose файл, настройте там связь базы данных и веб-приложения
добавьте в свой проект модели. Это могут быть те же модели, что были использованы для сохранения данных с открытого API, это может быть и что-то новое
добавьте возможность создавать новые записи
создайте страницу, на которой эти записи выводятся
база данных должна быть в отдельном контейнере
Flask приложение должно запускаться не в debug режиме, а в production-ready (uwsgi/gunicorn, nginx, Flask)

Критерии оценки:
docker-compose файл присутствует и работает
приложение взаимодействует с БД
в приложении есть возможность добавить записи, они сохраняются в БД
в приложении есть страница, которая выдаёт доступные записи (вытаскивает из БД)
Flask приложение настроено для запуска в production режиме (uwsgi, nginx, gunicorn)

"""

from contextlib import asynccontextmanager
import sys
import os

# Добавляем корневую папку проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio

from fastapi import FastAPI
import uvicorn


from src.core import create_tables
from src.routers.main_pages import router as main_pages_router
from src.routers.api_router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_pages_router, tags=["Main pages"])
app.include_router(api_router, tags=["API Router"])

#if __name__ == "__main__":
    # asyncio.run(create_tables())
    # uvicorn.run("main:app", reload=True)
    