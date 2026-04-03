import datetime
from typing import Annotated
import enum

# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    text,
)

from .base import Base, str_256
from .contact import Contact


# metadata_obj = MetaData()


created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.UTC),
    ),
]


class UsersOrm(Base):
    __tablename__ = "pd_users"

    username: Mapped[str] = mapped_column(String(20), unique=True)
    created_at: Mapped[created_at]

    sessions: Mapped[list["UserSessionsOrm"]] = relationship(back_populates="user")
    contacts: Mapped[list["ContactsOrm"]] = relationship(back_populates="user")


class UserSessionsOrm(Base):
    __tablename__ = "pd_usersessions"

    user_id: Mapped[int] = mapped_column(ForeignKey("pd_users.id", ondelete="SET NULL"))
    created_at: Mapped[created_at]
    logout_at: Mapped[updated_at]

    user: Mapped["UsersOrm"] = relationship(back_populates="sessions")


class Scope(enum.Enum):
    private = "private"
    public = "public"


class ContactsOrm(Base):
    __tablename__ = "pd_contacts"

    name: Mapped[str]
    phone: Mapped[str | None] = mapped_column(String(12))
    comment: Mapped[str_256 | None]
    scope: Mapped[Scope] = mapped_column(server_default=Scope.private.value)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("pd_users.id", ondelete="SET NULL")
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="contacts")

    def __init__(self, contact: Contact):
        super().__init__(
            name=contact.name,
            phone=contact.phone,
            comment=contact.comment,
            owner_id=contact.owner,
        )

    def __repr__(self):
        return f"""
            id: {self.id},
            name: {self.name},
            phone: {self.phone},
            comment: {self.comment},
            scope: {self.scope},
        """

    def to_contact(self) -> Contact:
        return Contact(
            id=str(self.id),
            name=self.name,
            phone=self.phone,
            comment=self.comment,
            owner=str(self.owner_id),
        )


# users_table = Table(
#     "pd_users",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("username", String),
#     Column("login_date", TIMESTAMP, server_default=func.now())
# )
