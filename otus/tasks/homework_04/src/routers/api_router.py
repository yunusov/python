from fastapi import APIRouter

from src.core import select_posts, add_post, load_json_data
from src.schemas.post import Post


router = APIRouter(prefix="/api/v1")

@router.post("/add")
async def add():
    """Добавить пост."""
    await add_post()

@router.post("/load")
async def load():
    """Загрузить посты."""
    await load_json_data()

@router.get("/posts", response_model=list[Post])
async def get_posts_list() -> list[Post]:
    """Получить список постов."""
    posts_orm = await select_posts() 
    return [Post.model_validate(post) for post in posts_orm]
