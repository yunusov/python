from fastapi import FastAPI
import uvicorn

from src.routers.main_pages import router as main_pages_router


app = FastAPI()
app.include_router(main_pages_router, tags=["Main pages"])

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
