from typing import List, Optional
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from src.models.users import User


async def get_by_id(db: AsyncSession, id: int) -> Optional[User]:
    result: Result = await db.execute(select(User).where(User.id==id))
    return result.first()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result: Result = await db.execute(select(User).where(User.email==email))
    return result.first()


async def filter(db: AsyncSession) -> List[User]:
    pass


async def create(db: AsyncSession):
    pass


async def update(db: AsyncSession):
    pass


async def delete(db: AsyncSession):
    pass