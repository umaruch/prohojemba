from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from src.core.settings import DatabaseSettings


class DatabaseComponents:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self.engine = create_async_engine(**settings.kwargs)
        self.sessionmaker = sessionmaker(bind=self.engine, class_=AsyncSession)