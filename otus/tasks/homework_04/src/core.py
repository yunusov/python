import asyncio
import random
import string
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from src.database import async_engine, connection
from src.jsonplaceholder_requests import fetch_posts_data, fetch_users_data
from src.models import BaseCls, UserOrm, PostOrm
from src.schemas.post import Post


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


@connection
async def select_posts(session) -> list[Post]:
    """Выбираем посты"""
    stmt = (
        select(PostOrm)
        .options(joinedload(PostOrm.user, innerjoin=True))
        .order_by(PostOrm.id.desc())
        .limit(100)
    )
    result = await session.execute(stmt)
    posts = result.unique().scalars().all()

    return [
        Post(
            id=post.id,
            title=post.title,
            user=post.user.username,
            body=post.body,
        )
        for post in posts
    ]


@connection
async def add_post(session):
    """Добавить пост"""
    userid = await get_user_id()

    title_len = random.randint(3, 10)
    body_len = random.randint(10, 50)
    str_gen = unique_str_generator()
    postOrm = PostOrm(
        user_id=userid,
        title=" ".join([next(str_gen) for _ in range(title_len)]),
        body=" ".join([next(str_gen) for _ in range(body_len)]),
    )
    session.add(postOrm)
    await session.commit()

@connection
async def get_user_id(session):
    """Получить id пользователя"""
    stmt = select(UserOrm.id).order_by(text("random()")).limit(1)
    result = await session.execute(stmt)
    userid = result.scalars().one_or_none()

    if not userid:
        userid = await create_user()
    return userid


@connection
async def create_user(session) -> int:
    """Создать пользователя"""
    userOrm = UserOrm(
        name="test_user", username="test_username", email="test_email.com"
    )
    session.add(userOrm)
    await session.commit()
    await session.refresh(userOrm)
    return userOrm.id


def unique_str_generator():
    """Генерирует случайную строку из букв и цифр."""
    while True:
        length = random.randint(1, 10)
        letters = string.ascii_uppercase + string.ascii_lowercase
        digits = string.digits
        random_string = "".join(
            random.choices(
                letters + digits, weights=[5] * len(letters) + [1] * len(digits), k=length
            )
        )
        yield random_string
