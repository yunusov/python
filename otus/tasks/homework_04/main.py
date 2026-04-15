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

from sqlalchemy import text

from src.models import BaseCls, UserOrm, PostOrm
from src.database import async_engine, connection
from src.jsonplaceholder_requests import fetch_posts_data, fetch_users_data


async def async_main():
    await create_tables()
    await load_json_data()


async def load_json_data():
    """Загружаем данные"""
    users_data: list[dict]
    posts_data: list[dict]
    # Создаем задачи для конкурентного выполнения
    task1 = asyncio.create_task(fetch_users_data())
    task2 = asyncio.create_task(fetch_posts_data())

    # Ожидаем завершения всех задач конкурентно
    users_data, posts_data = await asyncio.gather(task1, task2)
    await fulfill_users(users_data)
    await fulfill_posts(posts_data)


@connection
async def fulfill_users(users_data: list[dict], session):
    """Заполняем таблицу пользователей"""
    users_list = [
        UserOrm(
            username=user_data["username"],
            name=user_data["name"],
            email=user_data["email"],
        )
        for user_data in users_data
    ]
    session.add_all(users_list)
    await session.commit()


@connection
async def fulfill_posts(users_data: list[dict], session):
    """Заполняем таблицу постов"""
    posts_list = [
        PostOrm(
            user_id=user_data["userId"],
            title=user_data["title"],
            body=user_data["body"],
        )
        for user_data in users_data
    ]
    session.add_all(posts_list)
    await session.commit()


async def create_tables():
    """Подготовка таблиц"""
    async with async_engine.begin() as conn:
        query = await conn.execute(
            text(
                """SELECT 1
                 FROM information_schema.tables 
                WHERE table_schema = 'public' 
                  AND lower(table_name) IN ('hw4_users', 'hw4_posts') """
            )
        )
        result = query.scalar()
        if result:
            await conn.execute(
                text("TRUNCATE hw4_users, hw4_posts RESTART IDENTITY CASCADE")
            )
        else:
            await conn.run_sync(BaseCls.metadata.drop_all)
            await conn.run_sync(BaseCls.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(async_main())
