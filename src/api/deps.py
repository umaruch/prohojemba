from typing import Generator, Type, Callable
from fastapi import Request, Depends
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession


from src.services import security
from src.repositories.base import BaseRepository


async def _get_db_session(req: Request) -> Generator[AsyncSession, None, None]:
    session: AsyncSession = req.app.state.db()
    try:
        yield session
    finally:
        await session.close()


async def get_redis_connection(req: Request) -> Redis: 
    return req.app.state.redis()
    

def get_repository(repo_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
        session = Depends(_get_db_session)
        ) -> BaseRepository:
            return repo_type(db_session=session)

    return _get_repo


def get_current_user_by_access_token(
    token: str = Depends(security.oauth2)
):
    """
        Получение информации о пользователе из access токена
    """
    pass