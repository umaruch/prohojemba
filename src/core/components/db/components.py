from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from src.core.settings import DatabaseSettings


class DatabaseComponents:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self.engine = create_async_engine(**settings.kwargs)
        self.sessionmaker = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.sessionmaker()

    async def disconnect(self) -> None:
        await self.engine.dispose()