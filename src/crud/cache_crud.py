from typing import Optional
from aioredis import Redis

from src.core.settings import settings

async def set_validation_code(redis: Redis, email: str, validation_type: str, code: str) -> None:
    await redis.set(f"{validation_type}:{email}", code)


async def get_validation_code(redis: Redis, email: str, validation_type: str) -> Optional[str]:
    code = await redis.get(f"{validation_type}:{email}")
    if isinstance(code, bytes):
        return code.decode("utf-8")


async def set_refresh_token(redis: Redis, token: str, user_id: int, session_uuid: str) -> None:
    await redis.set(f"{user_id}:{session_uuid}", token, ex=settings.application.REFRESH_TOKEN_EXPIRE_SECONDS)


async def get_refresh_token(redis: Redis, user_id: int, session_uuid: str) -> Optional[str]:
    token = await redis.get(f"{user_id}:{session_uuid}")
    if isinstance(token, bytes):
        return token.decode("utf-8")


async def delete_refresh_token(redis: Redis, user_id: int, session_uuid: str):
    # await redis.
    pass