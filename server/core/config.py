from pydantic import BaseSettings


class Settings(BaseSettings):
    # Базовые настройки
    DEBUG: bool = True

    API_STR: str = "/api/v1"
    SECRET_KEY: str

    # Настройки подключения к БД
    SQLALCHEMY_DB_URI: str

    # Настройки подключения к Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str

    # Настройки Mail
    

settings = Settings()