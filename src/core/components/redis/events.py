import logging
from fastapi import FastAPI


from src.core.settings import RedisSettings
from src.core.components.redis.components import RedisComponents


async def connect_to_redis(app: FastAPI, settings: RedisSettings) -> None:
    app.state.redis = RedisComponents(settings)


async def close_redis_connection(app: FastAPI) -> None:
    await app.state.redis.disconnect()
