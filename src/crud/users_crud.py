from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


from src.models.users import User
from src.models.profiles import Profile

async def create_user(db: AsyncSession, email: str, password_hash: str, username: str) -> int:
    user = User(email=email, password_hash=password_hash, profile=Profile(username=username))
    db.add(user)
    await db.flush()
    print(user)
    return user.id



async def get_user_by_id(db: AsyncSession, user_id: int, with_profile: bool = False) -> User:
    if with_profile:
        sql = select(User).where(User.id==user_id).options(selectinload(User.profile))
    else:
        sql = select(User).where(User.id==user_id)

    return (await db.execute(sql)).scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    sql = select(User).where(User.email==email)
    return (await db.execute(sql)).scalars().first()


async def get_profile_by_username(db: AsyncSession, username: str) -> Optional[Profile]:
    sql = select(Profile).where(Profile.username==username)
    return (await db.execute(sql)).scalars().first()