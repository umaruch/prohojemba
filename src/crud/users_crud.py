from typing import List, Optional
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert
from fastapi import status
from fastapi.exceptions import HTTPException


from src.models.users import User


async def get_by_id(db: AsyncSession, id: int) -> Optional[User]:
    result: Result = await db.execute(select(User).where(User.id==id))
    return result.first()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result: Result = await db.execute(select(User).where(User.email==email))
    return result.scalars().first()


async def filter(db: AsyncSession) -> List[User]:
    pass


async def create(db: AsyncSession, **columns) -> User:
    try:
        user = User(**columns)
        db.add(user)
        await db.commit()
        return user
    except IntegrityError as err:
        await db.rollback()
        err_msg = err.args[0]
        if "duplicate key value violates unique constraint \"users_username_key\"" in err_msg:
            message = "Пользователь с таким именем уже существует"
        elif "duplicate key value violates unique constraint \"ix_users_email\"" in err_msg:
            message = "Пользователь с таким email уже существует"
        else:
            print(err)
            message = "Неизвестная ошибка"

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


async def update(db: AsyncSession):
    pass


async def delete(db: AsyncSession):
    pass