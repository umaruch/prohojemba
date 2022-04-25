import pathlib


from pydantic import BaseSettings


BASE_DIR = pathlib.Path(__file__).resolve().parent().parent().parent()
ENV_PATH = BASE_DIR / ".env" 


class Base(BaseSettings):
    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

class MailSettings(Base):
    """
        Настройки, необходимые для отправки писем на email
    """
    pass


class DatabaseSettings(Base):
    pass


class ApplicationSettings(Base):
    pass


class Settings:
    application: ApplicationSettings = ApplicationSettings()
    database: DatabaseSettings = DatabaseSettings()
    mail: MailSettings = MailSettings()

