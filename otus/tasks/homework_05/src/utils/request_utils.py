from fastapi import HTTPException, status
import httpx

from src.config import SERVER_URL
from src.utils.loguru_config import AppLogger

logger = AppLogger().get_logger()


async def async_request(method: str, url: str, params=None) -> str:
    """Вызов запроса определённого типа"""
    logger.info(f"{method = }; {url = }; {params = };")
    async_url = url
    if "http" not in url:
        async_url = SERVER_URL + url

    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            result = await client.get(async_url, params=params)
        elif method.upper() == "DELETE":
            result = await client.delete(async_url, params=params)
        elif method.upper() == "PUT":
            result = await client.put(async_url, params=params)
        elif method.upper() == "POST":
            result = await client.post(async_url, params=params)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неопознанный метод запроса '{method}'",
            )
        logger.info(f"{result = }")
        return result.json()
