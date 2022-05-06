from typing import Callable
from fastapi import FastAPI


from src.core.settings import Settings
from src.core.components.db.events import connect_to_db, close_all_db_connections
from src.core.components.redis.events import  connect_to_redis, close_redis_connection


def create_startup_handler(app: FastAPI, settings: Settings) -> Callable:
    async def start_app() -> None:
        # Отсюдова запускаются функции, которые надо выполнить при включении сервера
        await connect_to_db(app, settings.database)
        await connect_to_redis(app, settings.redis)

    return start_app


def create_shutdown_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        # Отсюдова запускаются функции, которые надо выполнить при отключении сервера
        await close_all_db_connections(app)
        await close_redis_connection(app)

    return stop_app