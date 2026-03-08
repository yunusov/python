from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", name="home", status_code=status.HTTP_200_OK)
async def index(request: Request):
    """Запрос home"""
    context = {"author": "Vitaly Yunusov",
               "course": "Python Basic Developer",
               "school": "Otus",
               "year": 2026}
    return context


@router.get("/ping/", name="ping", status_code=status.HTTP_200_OK)
async def index(request: Request):
    """Запрос PING"""
    return {"message": "pong"}

