from typing import Callable
from fastapi import FastAPI


from src.core.settings import Settings
from src.core.components.db.events import connect_to_db, close_all_db_connections


def create_startup_handler(app: FastAPI, settings: Settings) -> Callable:
    async def start_app() -> None:
        # Отсюдова запускаются функции, которые надо выполнить при включении сервера
        await connect_to_db(app, settings)

    return start_app


def create_shutdown_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        # Отсюдова запускаются функции, которые надо выполнить при отключении сервера
        await close_all_db_connections(app)

    return stop_app