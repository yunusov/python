from fastapi import APIRouter, Form, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.queries.core import get_user_by_name
from src.utils.loguru_config import AppLogger
from src.utils.request_utils import async_request

logger = AppLogger().get_logger()
router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, name="home")
async def index(request: Request):
    """Запрос полного списка пользователей"""
    user_id = request.session.get("user_id", None)
    if user_id:
        return await _response_index_html(request)
    else:
        return templates.TemplateResponse(request, "index.html")


@router.post("/login/", response_class=HTMLResponse, name="login")
async def enter_name(
    request: Request,
    username: str = Form(""),
):
    """Логирование пользователя"""
    if username.strip() == "":
        return templates.TemplateResponse(request, "index.html")

    request.session["username"] = username
    user = get_user_by_name(username)
    request.session["user_id"] = user.id
    return await _response_index_html(request)


@logger.catch(reraise=True)
async def _response_index_html(request: Request, ctx: dict = None):
    """GET-запрос для API /api/v1/contacts"""
    if ctx is None:
        ctx = {}
    contacts = {}
    user_id = request.session["user_id"]
    username = request.session["username"]
    if user_id:
        contacts = await async_request("GET", "/api/v1/contacts", {"user_id": user_id})

    logger.info(contacts)
    context = {
        "username": username,
        "user_id": user_id,
        "contacts": contacts,
        "error_message": (
            contacts.get("error_message", "")
            if isinstance(contacts, dict) is dict
            else ""
        ),
        **ctx,
    }
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
    request.session["user_id"] = None
    context = {"username": "", "user_id": ""}
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/search/", response_class=HTMLResponse)
async def search(
    request: Request, search_str: str = Query(None, description="Строка для поиска")
):
    """GET-запрос для API /api/v1/contacts"""
    contacts = {}
    user_id = request.session["user_id"]
    username = request.session["username"]
    if user_id:
        contacts = await async_request(
            "GET", "/api/v1/search", {"user_id": user_id, "search_str": search_str}
        )

    logger.info(contacts)
    context = {
        "user_id": user_id,
        "username": username,
        "contacts": contacts if contacts else [],
        "search_request": search_str,
        "search_records": len(contacts) if contacts else "0",
    }
    return templates.TemplateResponse(request, "index.html", context)
