from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_ASYNC,
    echo=True,
    connect_args={
        "ssl": False,
        "statement_cache_size": 0,
        "server_settings": {"search_path": "alembic_schema"},
    },
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


def connection(method):
    """Для работы с async_session_factory"""

    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper
