from typing import AsyncGenerator, Callable, Type
from fastapi import Request, Depends
from aioredis import Redis, ConnectionPool

from src.redis.repositories.base import BaseRedisRepository


def _get_redis_pool(req: Request) -> ConnectionPool:
    return req.app.state.redis_pool


async def _get_redis_connection_from_pool(
    redis_pool: ConnectionPool = Depends(_get_redis_pool)
) -> AsyncGenerator[Redis, None]:
    try:
        redis = Redis(connection_pool=redis_pool)
        yield redis
    finally:
        await redis.close()


def get_redis_repository(repo_type: Type[BaseRedisRepository]) -> Callable:
    def _get_repo(redis: Redis = Depends(_get_redis_connection_from_pool)) -> BaseRedisRepository:
        return repo_type(redis)

    return _get_repo
