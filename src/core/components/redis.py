import aioredis
from fastapi import FastAPI


from src.core.settings import Settings


def connect(app: FastAPI, settings: Settings) -> None:
    app.state.redispool = aioredis.BlockingConnectionPool.from_url(settings.redis.URL, max_connections=10)


async def disconnect(app: FastAPI) -> None:
    await app.state.redispool.disconnect()
    