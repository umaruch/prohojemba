from enum import Enum
from pydantic import BaseSettings


class AppEnvTypes(Enum):
    Production: str = "prod"
    Development: str = "dev"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.Production

    class Config:
        env_file = ".env"