from typing import Callable
from fastapi import FastAPI


from src.core.settings import Settings
from src.core.components import db, redis


def create_startup_handler(app: FastAPI, settings: Settings) -> Callable:
    async def start_app() -> None:
        # Отсюдова запускаются функции, которые надо выполнить при включении сервера
        db.connect(app, settings)
        redis.connect(app, settings)

    return start_app


def create_shutdown_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        # Отсюдова запускаются функции, которые надо выполнить при отключении сервера
        await db.disconnect(app)
        await redis.disconnect(app)

    return stop_app