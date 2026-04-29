from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.request_utils import async_request

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse, name="home")
async def index(request: Request):
    """Запрос полного списка пользователей"""
    return await _response_index_html(request)

@router.get("/add/", response_class=HTMLResponse, name="add_user")
async def add_post(request: Request):
    """Добавить пользователей"""
    await async_request("POST", "/api/v1/add", {})
    return RedirectResponse(url=request.url_for("home"), status_code=303)

@router.get("/load/", response_class=HTMLResponse, name="load_posts")
async def load_posts(request: Request):
    """Загрузить посты"""
    await async_request("POST", "/api/v1/load", {})
    return RedirectResponse(url=request.url_for("home"), status_code=303)


async def _response_index_html(request: Request):
    """GET-запрос для API /api/v1/posts"""
    posts = await async_request("GET", "/api/v1/posts", {})
    context = {
        "posts": posts
    }
    return templates.TemplateResponse(request, "index.html", context)