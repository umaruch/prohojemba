from functools import lru_cache
from typing import Dict, Type

from src.core.settings.base import AppEnvTypes, BaseAppSettings
from src.core.settings.app import AppSettings
from src.core.settings.production import ProdAppSettings
from src.core.settings.development import DevAppSettings


environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.Production: ProdAppSettings,
    AppEnvTypes.Development: DevAppSettings
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    settings = environments[app_env]
    return settings()