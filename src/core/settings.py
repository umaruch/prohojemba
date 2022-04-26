import pathlib
from typing import Optional, Dict, Any


from pydantic import BaseSettings, Field, validator, PostgresDsn

# Ставить False если работает релизная версия
DEBUG = True

BASE_DIR = pathlib.Path(__file__).resolve().parent().parent().parent()
ENV_PATH = BASE_DIR / ".env" 


class Base(BaseSettings):
    def to_kwargs(self):
        """
            Преобразование атрибутов в словарь аргументов
        """
        pass

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"


class MailSettings(Base):
    """
        Настройки, необходимые для отправки писем на email
    """
    pass


class LoggingSettings(Base):
    pass


class DatabaseSettings(Base):
    HOST: str = Field("127.0.0.1", env="POSTGRES_HOST")
    USER: str = Field(..., env="POSTGRES_USER")
    PASS: str = Field(..., env="POSTGRES_PASS")
    NAME: str = Field(..., env="POSTGRES_NAME") # Имя базы данных
    URL: Optional[str]
    ECHO: bool = DEBUG # Отображения выполняемого SQL в логах
 
    @validator("URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        
        return PostgresDsn.build(
            scheme="postgresql", host=values.get("HOST"), path=f"/{values.get('NAME') or ''}",
            user=values.get("USER"), password=values.get("PASS")
        ).replace("postgresql", "postgresql+asyncpg")
        

    def to_kwargs(self) -> Dict:
        return {
            "url": self.URL,
            "echo": self.ECHO
        }


class ApplicationSettings(Base):
    APP_NAME: str = "Prohojemba"
    VERSION: str = "0.0.1"
    DEBUG: bool = DEBUG
    API_URL: str = "/api/v1"
    SECRET_KEY: str = Field(..., "SECRET_KEY")


class Settings:
    application: ApplicationSettings = ApplicationSettings()
    database: DatabaseSettings = DatabaseSettings()
    mail: MailSettings = MailSettings()

