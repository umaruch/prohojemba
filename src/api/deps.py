from typing import Generator, Type, Callable
from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud import users_crud
from src.models.users import User
from src.services import security


async def get_db_session(req: Request) -> Generator[AsyncSession, None, None]:
    session: AsyncSession = req.app.state.db()
    try:
        yield session
    finally:
        await session.commit()
        await session.close()


def get_redis_connection(req: Request) -> Redis: 
    return req.app.state.redis()
    

async def get_current_user_by_access_token(
    db: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security.bearer)
) -> User:
    """
        Получение информации о пользователе из access токена
    """
    token = credentials.credentials
    user_id = security.decode_access_token(token)
    user = await users_crud.get_user_by_id(db, user_id)
    return user
    
    