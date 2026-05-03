from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool = False

    ENGINE: str
    NAME: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str

    @property
    def DEFAULT_DB_CONFIG(self):
        result = {
            "default": {
                "ENGINE": self.ENGINE,
                "NAME": self.NAME,
                "USER": self.USER,
                "PASSWORD": self.PASSWORD,
                "HOST": self.HOST,
                "PORT": self.PORT,
            }
        }
        return result

    model_config = SettingsConfigDict(env_file="config/.env")


settings = Settings()
