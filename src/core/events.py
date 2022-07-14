from typing import Callable
from fastapi import FastAPI

from src.core.settings.app import AppSettings


def create_start_app_handler(app: FastAPI, settings: AppSettings) -> Callable:
    async def on_startup() -> None:
        pass

    return on_startup


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def on_shutdown() -> None:
        pass

    return on_shutdown