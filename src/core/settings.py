import pathlib
import logging
from typing import Optional, Dict, Any


from pydantic import BaseSettings, Field, validator, PostgresDsn, EmailStr, RedisDsn

# Ставить False если работает релизная версия
DEBUG = True

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env" 


class Base(BaseSettings):
    @property
    def kwargs(self):
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
    SERVER: str = Field(..., env="MAIL_SERVER")
    PORT: int = Field(..., env="MAIL_PORT")
    USER: str = Field(..., env="MAIL_USER")
    PASS: str = Field(..., env="MAIL_PASS")
    USE_TLS: bool = True
    SENDER: EmailStr = Field(..., env="MAIL_SENDER") # Почта, с которой будут отсылаться сообщения

    @property
    def kwargs(self):
        return {
            "hostname": self.SERVER,
            "port": self.PORT,
            "username": self.USER,
            "password": self.PASS,
            "use_tls": self.USE_TLS
        }


class LoggingSettings(Base):
    LOGFILE_PATH: str = "server.logs" # Путь к файлу логов
    FILEMODE: str = "a"
    LEVEL: int = logging.DEBUG if DEBUG else logging.INFO
    DATE_FORMAT: str = "%d.%m.%Y %H:%M:%S"
    STR_FORMAT: str = "%(asctime)s - [%(levelname)s] - %(name)s  - %(message)s"
    
    @property
    def kwargs(self):
        return {
            "filename": self.LOGFILE_PATH,
            "filemode": self.FILEMODE,
            "level": self.LEVEL,
            "datefmt": self.DATE_FORMAT,
            "format": self.STR_FORMAT
        }


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
        
    @property
    def kwargs(self) -> Dict:
        return {
            "url": self.URL,
            "echo": self.ECHO
        }


class RedisSettings(Base):
    HOST: str = Field("localhost", env="REDIS_HOST")
    USER: str = Field(None, env="REDIS_USER")
    PASS: str = Field(None, env="REDIS_PASS")
    DB: int = Field(1, env="REDIS_DB")  

    URL: Optional[str]

    @validator("URL", pre=True)
    def assemble_redis_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("HOST"), path=f"/{values.get('DB')}",
            user=values.get("USER"), password=values.get("PASS")
        )

    @property
    def kwargs(self):
        return {
            "url": self.URL
        }


class ApplicationSettings(Base):
    APP_NAME: str = "Prohojemba"
    VERSION: str = "0.0.1"
    DEBUG: bool = DEBUG
    API_URL: str = "/api/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")

    @property
    def kwargs(self) -> Dict:
        return {
            "debug": self.DEBUG,
            "title": self.APP_NAME,
            "version": self.VERSION,
        }


class Settings:
    application: ApplicationSettings = ApplicationSettings()
    database: DatabaseSettings = DatabaseSettings()
    mail: MailSettings = MailSettings()
    redis: RedisSettings = RedisSettings()
    logging: LoggingSettings = LoggingSettings()

    def __init__(self) -> None:
        print("settings init")

settings = Settings()