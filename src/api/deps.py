from typing import AsyncGenerator
from fastapi import Request, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.services import security


async def get_db_session(req: Request) -> AsyncSession:
    db: AsyncSession = req.app.state.dbpool()
    try:
        yield db
    finally:
        await db.close()


async def get_redis_connection(req: Request) -> AsyncGenerator[Redis, None]: 
    """
        Получение соединения redis из пула, обработка возможных ошибок в ходе работы и освобождение соединения

        TODO ДОбавить обработку возможных ошибок
    """
    redis: Redis = Redis(connection_pool=req.app.state.redispool)
    try:
        yield redis
    finally:
        await redis.close()
    

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security.bearer)
) -> User:
    """
        TODO Получение информации о пользователе из access токена
    """
    try:
        token = credentials.credentials
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token is missing"
        )
    return security.get_user_by_access_token(db, token)