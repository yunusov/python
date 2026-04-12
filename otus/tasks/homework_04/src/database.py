import asyncio

import asyncpg

from src.models import BaseCls

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import ssl
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import settings

# asyncio.run(get_version_async())

ca_path = Path("src/.cert/supabase-ca.crt").resolve()
print(f"{settings.DATABASE_URL_ASYNC=}")
print(f"{ca_path=}")
print(ca_path.exists(), ca_path.is_file())
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_REQUIRED

ssl_context.load_verify_locations(cafile=str(ca_path))

if hasattr(ssl, "VERIFY_X509_STRICT"):
    ssl_context.verify_flags &= ~ssl.VERIFY_X509_STRICT

async_engine = create_async_engine(
    url=settings.DATABASE_URL_ASYNC,
    echo=True,
    connect_args={
        "ssl": ssl_context,
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0
    },
    execution_options={"isolation_level": "AUTOCOMMIT"},
    poolclass=NullPool,
)
print(f"{async_engine=}")
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
print(f"{async_session_factory=}")


async def main():
    # pool = await asyncpg.create_pool(
    #     dsn=settings.DATABASE_URL_ASYNC.replace("postgresql+asyncpg://", "postgresql://"),
    #     min_size=1,
    #     max_size=1,
    #     ssl=ssl_context,
    #     statement_cache_size=0
    # )

    # async with pool.acquire() as conn:
    #     v = await conn.fetchval("select 1")

    #     print("OK:", v)

    # await pool.close()


    dsn = settings.DATABASE_URL_ASYNC.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(dsn=dsn, ssl=ssl_context, statement_cache_size=0)
    try:
        v = await conn.fetchval("select current_schema()")
        print("OK current_schema =", v)
        await conn.execute("create table tt (id int);")
    finally:
        await conn.close()
