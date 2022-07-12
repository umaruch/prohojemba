from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_activities(db: AsyncSession, user_id: int, limit: int, offset: int):
    pass