from typing import Any, List, Optional, Dict
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, update as _update, delete as _delete
from fastapi import status
from fastapi.exceptions import HTTPException


from src.models.users import User


async def get_by_id(db: AsyncSession, id: int) -> Optional[User]:
    result: Result = await db.execute(select(User).where(User.id==id))
    return result.scalars().first()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result: Result = await db.execute(select(User).where(User.email==email))
    return result.scalars().first()


async def filter(db: AsyncSession) -> List[User]:
    pass


async def create(db: AsyncSession, **columns: Any) -> int:
    try:
        user = User(**columns)
        db.add(user)
        await db.commit()
        return user.id
    except IntegrityError as err:
        raise await _handle_users_error(db, err)


async def update(db: AsyncSession, id: int, **columns: Any) -> None:
    try:
        await db.execute(_update(User).where(User.id==id).values(**columns).returning(None))
        await db.commit()
    except IntegrityError as err:
        raise await _handle_users_error(db, err)


async def _handle_users_error(db: AsyncSession, err: Exception) -> HTTPException:
    await db.rollback()
    err_msg = err.args[0]
    if "duplicate key value violates unique constraint \"users_username_key\"" in err_msg:
        message = "Пользователь с таким именем уже существует"
    elif "duplicate key value violates unique constraint \"ix_users_email\"" in err_msg:
        message = "Пользователь с таким email уже существует"
    else:
        print(err)
        message = "Неизвестная ошибка"

    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )