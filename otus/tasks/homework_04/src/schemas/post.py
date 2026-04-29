from pydantic import BaseModel

class Post(BaseModel):
    id: int
    user: str
    title: str
    body: str