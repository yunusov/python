from fastapi import APIRouter, Query

from src.queries.core import (
    select_contacts,
    get_contact_by_id,
    create_contact,
    modify_contact,
    delete_contact,
)
from src.models.contact import Contact
from src.utils.loguru_config import AppLogger

logger = AppLogger().get_logger()
router = APIRouter()


@router.get("/contacts", response_model=list[Contact])
async def get_contacts_list(user_id: str = Query("", description="ID пользователя")):
    """Получить список контактов."""
    contacts_orm = select_contacts(p_owner=user_id)
    result = [contact_orm.to_contact() for contact_orm in contacts_orm]
    return result


@router.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(
    contact_id: str, user_id: str = Query("", description="ID пользователя")
):
    """Получить данные контакта."""
    orm_contact = get_contact_by_id(contact_id, user_id)
    result = orm_contact.to_contact()

    logger.info(f"{user_id = }; {contact_id = }; {result = }")
    return result


@router.post("/contacts", response_model=Contact)
async def add_contact(
    user_id: str = Query(None, description="user_id"),
    name: str = Query(None, description="Имя контакта"),
    phone: str = Query("", description="Телефонный номер контакта"),
    comment: str = Query("", description="Комментарий для контакта"),
):
    """Добавить контакт"""
    logger.info(f"{name =}; {phone = }; {comment = }; {user_id = }")
    contact = Contact(
        id=str(id), name=name, phone=phone, comment=comment, owner=str(user_id)
    )
    create_contact(contact)

    return contact


@router.put("/contacts")
async def edit_contact(
    contact_id: str = Query(None, description="ID контакта"),
    user_id: str = Query(None, description="user_id"),
    name: str = Query(None, description="Имя контакта"),
    phone: str = Query("", description="Телефонный номер контакта"),
    comment: str = Query("", description="Комментарий для контакта"),
):
    """Изменить контакт"""
    if user_id:
        contact = Contact(
            id=contact_id,
            name=name,
            phone=phone,
            comment=comment,
            owner=user_id,
        )
        modify_contact(contact)
    return {}


@router.delete("/contacts/{contact_id}")
async def remove_contact(
    contact_id: str,
    user_id: str = Query(None, description="user_id"),
):
    """Удалить контакт"""
    delete_contact(contact_id, user_id)
    return {}


@router.get("/search")
async def search_contacts(
    user_id: str = Query(None, description="user_id"),
    search_str: str = Query(None, description="Строка для поиска"),
):
    """Найти контакты"""
    logger.info(f"{user_id=}, {search_str=}")
    if user_id:
        result = select_contacts(p_owner=user_id, p_filter=search_str)
        return result
