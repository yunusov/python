from fastapi import APIRouter, Form, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.loguru_config import AppLogger

logger = AppLogger().get_logger()

from src.utils.request_utils import async_request

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, name="home")
async def index(request: Request):
    """Запрос полного списка пользователей"""
    username = request.session.get("username", None)
    if username:
        return await _response_index_html(request, username)
    else:
        return templates.TemplateResponse(request, "index.html")


@router.post("/login/", response_class=HTMLResponse, name="login")
async def enter_name(
    request: Request,
    username: str = Form(""),
):
    """Логирование пользователя"""
    request.session["username"] = username
    return await _response_index_html(request, username)


@logger.catch(reraise=True)
async def _response_index_html(request: Request, username: str):
    """GET-запрос для API /api/v1/contacts"""
    contacts = {}
    if username:
        contacts = await async_request(
            "GET", "/api/v1/contacts", {"username": username}
        )

    context = {"username": username, "contacts": contacts}
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/about/", response_class=HTMLResponse, name="html_about")
async def about(request: Request):
    """Вызов страницы about.html"""
    context = {"title": "О программе"}
    return templates.TemplateResponse(request, "about.html", context)


@router.get("/reset/", response_class=HTMLResponse)
async def user_reset(request: Request):
    """Разлогирование пользователя"""
    request.session["username"] = None
    context = {"username": ""}
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/search/", response_class=HTMLResponse)
async def search(
    request: Request, search_str: str = Query(None, description="Строка для поиска")
):
    username = request.session["username"]

    return await _response_search(request, username, search_str)


@logger.catch(reraise=True)
async def _response_search(request: Request, username: str, search_str: str):
    """GET-запрос для API /api/v1/contacts"""
    contacts = {}
    if username:
        contacts = await async_request(
            "GET", "/api/v1/search", {"username": username, "search_str": search_str}
        )

    context = {
        "username": username,
        "contacts": contacts,
        "search_request": search_str,
        "search_records": len(contacts),
    }
    return templates.TemplateResponse(request, "index.html", context)
