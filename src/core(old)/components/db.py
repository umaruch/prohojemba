from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from src.core.settings import DatabaseSettings


def connect(app: FastAPI, settings: DatabaseSettings) -> None:
    app.state.engine = create_async_engine(**settings.kwargs)
    app.state.dbpool = sessionmaker(app.state.engine, expire_on_commit=False, class_=AsyncSession)


async def disconnect(app: FastAPI) -> None:
    await app.state.engine.dispose()