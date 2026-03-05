from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.loguru_config import AppLogger
from src import phone_dict
from .main_pages import _response_index_html

logger = AppLogger().get_logger()

from src.utils.request_utils import async_request

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/contact/{contact_id}/", response_class=HTMLResponse)
async def contact(request: Request, contact_id: str):
    """Вызов страницы contact.html"""
    username = request.session["username"]
    return await _response_contact(request, username, contact_id)


@router.get("/create/", response_class=HTMLResponse, name="create")
async def create_contact(
    request: Request,
):
    """Переход на страницу создания пользователя"""
    context = {
        "operation": "Создание",
        "action": "create",
        "name": "",
        "phone": "",
        "comment": "",
        "id": "",
    }
    return templates.TemplateResponse(request, "create_contact.html", context)


@router.get("/edit/{contact_id}/", response_class=HTMLResponse, name="create")
async def create_contact(
    contact_id: str,
    request: Request,
):
    """Переход на страницу редактирования пользователя"""
    contact = phone_dict.get_contact(contact_id)
    if contact:
        name = contact["name"]
        phone = contact["phone"]
        comment = contact["comment"]
    context = {
        "operation": "Редактирование",
        "action": "modify",
        "name": name,
        "phone": phone,
        "comment": comment,
        "id": contact_id,
    }
    return templates.TemplateResponse(request, "create_contact.html", context)


@router.post("/create/", response_class=HTMLResponse, name="create")
async def create_contact(
    request: Request,
    name: str = Form(None, description="Имя контакта"),
    phone: str = Form("", description="Телефонный номер контакта"),
    comment: str = Form("", description="Комментарий для контакта"),
):
    """Вызов API создания пользователя"""
    username = request.session["username"]
    context = {"username": username, "name": name, "phone": phone, "comment": comment}
    logger.info(f"{context = }")
    if username:
        await async_request("POST", "/api/v1/contacts", context)
    return await _response_index_html(request, username)


@router.post("/modify/", response_class=HTMLResponse, name="modify")
async def create_contact(
    request: Request,
    id: str = Form(None, description="ID контакта"),
    name: str = Form(None, description="Имя контакта"),
    phone: str = Form("", description="Телефонный номер контакта"),
    comment: str = Form("", description="Комментарий для контакта"),
):
    """Вызов API создания пользователя"""
    username = request.session["username"]
    context = {
        "username": username,
        "name": name,
        "phone": phone,
        "comment": comment,
        "contact_id": id,
    }
    logger.info(f"{context = }")
    if username:
        await async_request("PUT", "/api/v1/contacts", context)
    return await _response_index_html(request, username)


@router.get("/delete/{contact_id}/")
async def delete_client(contact_id: str, request: Request):
    """Удалить контакт"""
    username = request.session["username"]
    await async_request(
        "DELETE", f"/api/v1/contacts/{contact_id}", {"username": username}
    )
    return await _response_index_html(request, username)


@logger.catch(reraise=True)
async def _response_contact(request: Request, username: str, contact_id: str):
    """GET-запрос для API /api/v1/contacts/{contact_id}"""
    contacts = {}
    if username:
        contacts = await async_request(
            "GET",
            f"/api/v1/contacts/{contact_id}",
            {"username": username},
        )

    logger.info(f"{type(contacts)}")
    logger.info(f"{contacts = }")
    context = {"username": username, "contact": contacts}
    return templates.TemplateResponse(request, "contact.html", context=context)
