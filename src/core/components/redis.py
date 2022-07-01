import aioredis
from fastapi import FastAPI


from src.core.settings import RedisSettings


def connect(app: FastAPI, settings: RedisSettings) -> None:
    app.state.redispool = aioredis.BlockingConnectionPool.from_url(**settings.kwargs)


async def disconnect(app: FastAPI) -> None:
    await app.state.redispool.disconnect()
    