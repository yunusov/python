from fastapi import APIRouter, Query

from src import phone_dict
from src.models.contact import Contact
from src.utils.loguru_config import AppLogger

logger = AppLogger().get_logger()

router = APIRouter()


@router.get("/contacts", response_model=list[Contact])
async def get_contacts_list(username: str = Query("", description="Имя пользователя")):
    """Получить список контактов."""
    result = phone_dict.get_contacts_list()
    logger.info(f"{username = }; {result = }")
    if username:
        result = [
            contact
            for contact in result
            if contact["owner"] == username
            or contact["owner"] == ""
            or username.lower() == "admin"
        ]
    logger.info(f"{result = }")
    return result


@router.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(
    contact_id: str, username: str = Query("", description="Имя пользователя")
):
    """Получить данные контакта."""
    result = phone_dict.get_contacts_list()

    logger.info(f"{username = }; {contact_id = }; {result = }")

    if username:
        result = [
            contact
            for contact in result
            if (
                contact["owner"] == username
                or contact["owner"] == ""
                or username.lower() == "admin"
            )
            and contact["id"] == contact_id
        ]

    return result[0]


@router.post("/contacts", response_model=Contact)
async def add_contact(
    username: str = Query(None, description="username"),
    name: str = Query(None, description="Имя контакта"),
    phone: str = Query("", description="Телефонный номер контакта"),
    comment: str = Query("", description="Комментарий для контакта"),
):
    """Добавить контакт"""
    id = phone_dict.get_next_id()
    logger.info(f"{name =}; {phone = }; {comment = }; {username = }")
    contact = Contact(id=id, name=name, phone=phone, comment=comment, owner=username)
    phone_dict.append_contact(contact)

    return contact


@router.put("/contacts")
async def modify_contact(
    contact_id: str = Query(None, description="ID контакта"),
    username: str = Query(None, description="username"),
    name: str = Query(None, description="Имя контакта"),
    phone: str = Query("", description="Телефонный номер контакта"),
    comment: str = Query("", description="Комментарий для контакта"),
):
    """Изменить контакт"""
    if username:
        result = phone_dict.get_contact(contact_id)
        if result:
            phone_dict.delete_contact(result)
            contact = Contact(
                id=contact_id,
                name=name,
                phone=phone,
                comment=comment,
                owner=username,
            )
            phone_dict.append_contact(contact)
            return contact
    return {}


@router.delete("/contacts/{contact_id}")
async def delete_contact(
    contact_id: str, username: str = Query(None, description="username")
):
    """Удалить контакт"""
    if username:
        result = phone_dict.get_contacts_list()
        result = [
            contact
            for contact in result
            if (
                contact["owner"] == username
                or contact["owner"] == ""
                or username.lower() == "admin"
            )
            and contact["id"] == contact_id
        ]
        if result:
            phone_dict.delete_contact(result[0])
            return {"message": f"Контакт {contact_id} был удален"}
    return {}


@router.get("/search")
async def search_contacts(
    username: str = Query(None, description="username"),
    search_str: str = Query(None, description="username"),
):
    """Найти контакты"""
    if username:
        result = phone_dict.get_contacts_list()
        result = [
            contact
            for contact in result
            if (
                contact["owner"] == username
                or contact["owner"] == ""
                or username.lower() == "admin"
            )
            and (search_str in contact["name"] or
                 search_str in contact["phone"] or
                 search_str in contact["comment"] or
                 search_str == contact["id"])
        ]
        return result
