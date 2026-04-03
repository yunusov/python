from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.queries.core import get_contact_by_id
from src.utils.loguru_config import AppLogger
from src.utils.request_utils import async_request
from .main_pages import _response_index_html

logger = AppLogger().get_logger()

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/create/", response_class=HTMLResponse, name="create")
async def navigate_to_create_contact(
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
async def edit_contact(
    contact_id: str,
    request: Request,
):
    """Переход на страницу редактирования пользователя"""
    contact = get_contact_by_id(contact_id, request.session["user_id"])
    if contact:
        context = {
            "operation": "Редактирование",
            "action": "modify",
            "name": contact.name,
            "phone": contact.phone,
            "comment": contact.comment,
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
    user_id = request.session["user_id"]
    context = {"user_id": user_id, "name": name, "phone": phone, "comment": comment}
    logger.info(f"{context = }")
    if user_id:
        contact = await async_request("POST", "/api/v1/contacts", context)
        logger.info(contact)
        context.update(contact)
    return await _response_index_html(request, context)


@router.post("/modify/", response_class=HTMLResponse, name="modify")
async def modify_contact(
    request: Request,
    id: str = Form(None, description="ID контакта"),
    name: str = Form(None, description="Имя контакта"),
    phone: str = Form("", description="Телефонный номер контакта"),
    comment: str = Form("", description="Комментарий для контакта"),
):
    """Вызов API создания пользователя"""
    user_id = request.session["user_id"]
    context = {
        "user_id": user_id,
        "name": name,
        "phone": phone,
        "comment": comment,
        "contact_id": id,
    }
    logger.info(f"{context = }")
    if user_id:
        context = await async_request("PUT", "/api/v1/contacts", context)
    return await _response_index_html(request, context)


@router.get("/delete/{contact_id}/")
async def delete_client(contact_id: str, request: Request):
    """Удалить контакт"""
    user_id = request.session["user_id"]
    await async_request(
        "DELETE", f"/api/v1/contacts/{contact_id}", {"user_id": user_id}
    )
    return await _response_index_html(request)
