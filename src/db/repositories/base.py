from sqlalchemy.ext.asyncio import AsyncSession


class BaseDatabaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session