from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Базовые настройки
    DEBUG: bool = True

    API_STR: str = "/api/v1"
    SECRET_KEY: str

    # Настройки подключения к БД
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    SQLALCHEMY_DB_URI: str | None = None

    # Настройки подключения к Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "1"

    # Получение URL базы данных
    @validator("SQLALCHEMY_DB_URI", pre=True)
    def assemble_db_uri(cls, v, values) -> str:
        if isinstance(v, str):
            return v

        # Место под драйвер БД остается пустым, так как 
        # alembic и сервер используют разные драйвера
        return "postgresql+{}://%s:%s@%s/%s" % (
            values.get("POSTGRES_USER"),
            values.get("POSTGRES_PASS"),
            values.get("POSTGRES_SERVER", "localhost"),
            values.get("POSTGRES_DB")
        )

    class Config:
        env_file = ".env"
            

settings = Settings()
print(settings.SQLALCHEMY_DB_URI)