from typing import AsyncGenerator, Callable, Type
from fastapi import Request, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


from src.db.repositories.base import BaseDatabaseRepository


def _get_database_pool(req: Request) -> sessionmaker:
    return req.app.state.db_pool


async def _get_database_connection_from_pool(db_pool: sessionmaker = Depends(_get_database_pool)) -> AsyncGenerator[AsyncSession, None]:
    try:
        session = db_pool()
        yield session
    finally:
        session.close()


def get_database_repository(repo_type: Type[BaseDatabaseRepository]) -> Callable:
    def _get_repo(
            db_session: AsyncSession = Depends(
                _get_database_connection_from_pool)
    ) -> BaseDatabaseRepository:
        return repo_type(db_session)

    return _get_repo
