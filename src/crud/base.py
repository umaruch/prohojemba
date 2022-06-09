from sqlalchemy.ext.asyncio import AsyncSession


from src.models.base import Base


class BaseCRUD:
    def __init__(self, session: AsyncSession) -> None:
        pass