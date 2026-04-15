"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

from typing import Annotated

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

import os

PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

Base = None
Session = None

metadata_obj = MetaData()
int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class BaseCls(DeclarativeBase):
    id: Mapped[int_pk]
    metadata = metadata_obj


class UserOrm(BaseCls):
    """Класс-пользователя"""

    __tablename__ = "hw4_users"

    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str]

    posts: Mapped[list["PostOrm"]] = relationship(back_populates="user")


class PostOrm(BaseCls):
    """Класс-пост"""

    __tablename__ = "hw4_posts"

    user_id: Mapped[int] = mapped_column(ForeignKey("hw4_users.id", ondelete="CASCADE"))
    title: Mapped[str]
    body: Mapped[str]

    user: Mapped["UserOrm"] = relationship(back_populates="posts")
