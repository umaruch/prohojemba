from typing import Callable
from fastapi import FastAPI


from src.core.settings import Settings
from src.core.components.db.events import connect_to_db


def create_startup_handler(app: FastAPI, settings: Settings) -> Callable:
    async def start_app() -> None:
        # Здесь подключяются дополнительные компоненты
        await connect_to_db(app, settings)

    return start_app