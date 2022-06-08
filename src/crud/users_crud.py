from typing import Optional, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder


from src.crud.base import BaseCRUD
from src.models.users import User
from src.models.profiles import Profile


users = BaseCRUD(User)


async def create_user(db: AsyncSession, email: str, password_hash: str, username: str) -> int:
    user = User(email=email, password_hash=password_hash, profile=Profile(username=username))
    db.add(user)
    await db.commit()
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


async def update_user(db: AsyncSession, user: Union[User, int], update_data: Dict) -> None:
    if isinstance(user, int):
        sql = update(User).where(User.id==user).values(**update_data)
    else:
        sql = update(User).where(User.id==user.id).values(**update_data)

    await db.execute(sql)
    await db.commit()  