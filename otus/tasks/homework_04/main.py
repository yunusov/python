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
"""

import asyncio

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from sqlalchemy import text

from src.models import BaseCls
from src.database import main, async_engine
from src.jsonplaceholder_requests import fetch_posts_data, fetch_users_data


async def async_main():
    # await load_json_data()
    # await create_tables()
    await main()


async def load_json_data():
    users_data: list[dict]
    posts_data: list[dict]
    # Создаем задачи для конкурентного выполнения
    task1 = asyncio.create_task(fetch_users_data())
    task2 = asyncio.create_task(fetch_posts_data())

    # Ожидаем завершения всех задач конкурентно
    users_data, posts_data = await asyncio.gather(task1, task2)

    print(f"Результаты: {len(posts_data)=}")


async def create_tables():
    print("create_tables 1")
    async with async_engine.connect() as conn:
        #     await conn.run_sync(BaseCls.metadata.drop_all)
        #     await conn.run_sync(BaseCls.metadata.create_all)
        print("create_tables 2")
        await conn.execute(text("select 1"))

if __name__ == "__main__":
    asyncio.run(async_main())
