
from sqlalchemy import (
    or_,
    select,
)
from src.models.db_models import UsersOrm, UserSessionsOrm, ContactsOrm, Scope
from src.database import (
    sync_engine,
    session_factory,
)
from src.models import Base, Contact
from src.utils.loguru_config import AppLogger

logger = AppLogger().get_logger()


def create_tables():
    # metadata_obj.create_all(sync_engine)
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def insert_user():
    with session_factory() as session:
        user1 = UsersOrm(username="Y")
        user2 = UsersOrm(username="G")
        sess1 = UserSessionsOrm(user=user1)
        sess2 = UserSessionsOrm(user=user1)
        sess3 = UserSessionsOrm(user=user2)
        contact1 = ContactsOrm(
            name="contact1",
            phone="777",
            scope=Scope.private,
            user=user1,
        )
        contact4 = ContactsOrm(
            name="contact4",
            phone="7774",
            scope=Scope.public,
            user=user1,
        )
        contact2 = ContactsOrm(
            name="contact2",
            phone="7771",
            user=user2,
        )
        contact3 = ContactsOrm(
            name="contact3", phone="7772", user=user2, scope=Scope.public
        )
        session.add_all(
            [
                user1,
                user2,
                sess1,
                sess2,
                sess3,
                contact1,
                contact2,
                contact3,
                contact4,
            ]
        )
        session.commit()
    # with sync_engine.connect() as conn:
    #     stmt = insert(users_table).values(
    #         [
    #             {"username": "google"},
    #             {"username": "yandex"},
    #         ]
    #     )
    #     #stmt = text("insert into pd_users(username) values('g'),('y');")
    #     conn.execute(stmt)
    #     conn.commit()


def select_contacts(p_owner: str, p_filter: str = None) -> list[ContactsOrm]:
    """Получить список контактов"""
    with session_factory() as session:
        query = select(ContactsOrm).filter(
            or_(
                ContactsOrm.scope == Scope.public,
                ContactsOrm.owner_id == int(p_owner),
            ),
        )
        if p_filter:
            query = query.filter(
                or_(
                    ContactsOrm.id == int(p_filter),
                    ContactsOrm.name.like(f"%{p_filter}%"),
                    ContactsOrm.phone.like(f"%{p_filter}%"),
                    ContactsOrm.comment.like(f"%{p_filter}%"),
                ),
            )
        result = session.execute(query)
        contacts = result.scalars().all()
        return contacts


def get_contact_by_id(contact_id: str, owner_id: str) -> ContactsOrm:
    """Получить список контактов"""
    with session_factory() as session:
        query = select(ContactsOrm).filter(
            or_(
                ContactsOrm.scope == Scope.public,
                ContactsOrm.owner_id == int(owner_id),
            ),
            ContactsOrm.id == int(contact_id),
        )
        result = session.execute(query)
        contact = result.scalars().one_or_none()
        return contact


def get_user_by_name(username: str) -> UsersOrm:
    """Получить ИД пользователя"""
    with session_factory() as session:
        query = select(UsersOrm).filter_by(username=username)
        result = session.execute(query).scalar_one_or_none()
        if not result:
            result = UsersOrm(username=username)
            session.add(result)
            session.commit()
            session.refresh(result)
    return result


def create_contact(contact: Contact) -> ContactsOrm:
    """Создать контакт для пользователя"""
    with session_factory() as session:
        contact = ContactsOrm(contact)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        logger.info(f"Создан контакт {contact=}")
    return contact


def modify_contact(contact: Contact) -> ContactsOrm:
    """Изменить контакт пользователя"""
    with session_factory() as session:
        query = select(ContactsOrm).filter_by(
            owner_id=int(contact.owner), id=int(contact.id)
        )
        contact_orm = session.execute(query).scalar_one_or_none()
        if contact_orm:
            contact_orm.name = contact.name
            contact_orm.phone = contact.phone
            contact_orm.comment = contact.comment
            # to-do: contact_orm.scope = ???

            session.commit()
    return contact


def delete_contact(contact_id: str, user_id: str) -> ContactsOrm:
    """Удалить контакт пользователя"""
    with session_factory() as session:
        query = select(ContactsOrm).filter_by(owner_id=int(user_id), id=int(contact_id))
        contact_orm = session.execute(query).scalar_one_or_none()
        if contact_orm:
            session.delete(contact_orm)
            session.commit()
    return contact_id
