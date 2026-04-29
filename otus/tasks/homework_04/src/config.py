from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "pg"
    DB_PORT: int = 5432
    DB_USER: str = "app"
    DB_PASS: str = "password"
    DB_NAME: str = "blog"

    MIDDLEWARE_SECRET_KEY: str = "secret"
    SERVER_IP: str = "127.0.0.1"
    SERVER_PORT: str = "8000"

    @property
    def DATABASE_URL_ASYNC(self):
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASS)
        return f"postgresql+asyncpg://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SERVER_URL(self):
        return "http://" + self.SERVER_IP + ":" + self.SERVER_PORT

    model_config = SettingsConfigDict(env_file="src/.env")


settings = Settings()
