import logging

from src.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    title: str = "Проходжемба (DEV)"
    debug: bool = True

    logging_level: int = logging.DEBUG