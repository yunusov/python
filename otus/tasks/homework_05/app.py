"""
Домашнее задание №5
Первое веб-приложение

- в модуле `app` создайте базовое FastAPI приложение
- создайте обычные представления
  - создайте index view `/`
  - добавьте страницу `/about/`, добавьте туда текст, информацию о сайте и разработчике
  - создайте базовый шаблон (используйте https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template)
  - в базовый шаблон подключите статику Bootstrap 5 (подключите стили), примените стили Bootstrap
  - в базовый шаблон добавьте навигационную панель `nav` (https://getbootstrap.com/docs/5.0/components/navbar/)
  - в навигационную панель добавьте ссылки на главную страницу `/` и на страницу `/about/` при помощи `url_for`
  - добавьте новые зависимости в файл `requirements.txt` в корне проекта
    (лучше вручную, но можно командой `pip freeze > requirements.txt`, тогда обязательно проверьте, что туда попало, и удалите лишнее)
- создайте api представления:
  - создайте api router, укажите префикс `/api`
  - добавьте вложенный роутер для вашей сущности (если не можете придумать тип сущности, рассмотрите варианты: товар, книга, автомобиль)
  - добавьте представление для чтения списка сущностей
  - добавьте представление для чтения сущности
  - добавьте представление для создания сущности
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request, status
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from src.utils.loguru_config import AppLogger
from src.routers.main_pages import router as main_pages_router
from src.routers.api_router import router as api_router
from src.routers.operations import router as operations_router
from src import settings

logger = AppLogger().get_logger()
app = FastAPI()
app.mount("/images", StaticFiles(directory="src\\images"), name="images")
app.add_middleware(SessionMiddleware, secret_key=settings.MIDDLEWARE_SECRET_KEY)

app.include_router(main_pages_router, tags=["Main pages"])
app.include_router(operations_router, tags=["Contact operations"])
app.include_router(api_router, tags=["API contacts"], prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Внутренняя ошибка: {str(exc)}"}
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host=settings.SERVER_IP, port=int(settings.SERVER_PORT), reload=True)
