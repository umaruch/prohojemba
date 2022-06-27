from datetime import timedelta, datetime
import jwt
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis
from passlib.context import CryptContext


from src.core.settings import settings
from src.crud import users_crud
from src.models.users import User
from src.schemes import auth


pwd_context = CryptContext(schemes=["bcrypt"])
bearer = HTTPBearer()


def _get_password_hash(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def _verify_password(raw_password, hashed_password) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def _encode_access_token(user_id: int) -> str:
    created_at = datetime.utcnow()
    payload = {
        "exp": created_at + timedelta(minutes=30),
        "iat": created_at,
        "scope": "access_token",
        "sub": user_id
    }
    return jwt.encode(payload, key=settings.application.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> int:
    pass


async def _encode_refresh_token(user_id: int) -> str:
    pass


def decode_refresh_token(token: str) -> str:
    pass


def register_new_user(db: AsyncSession, redis: Redis, form: auth.SigninForm) -> auth.TokensPair:
    pass


async def authenticate_user(db: AsyncSession, redis: Redis, form: auth.LoginForm) -> auth.TokensPair:
    user = await users_crud.get_by_email(form.email)
    if user and _verify_password(form.password, user.encoded_password):
        return auth.TokensPair(
            access_token=_encode_access_token(user_id=user.id),
            refresh_token=_encode_refresh_token(user_id=user.id))

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )


async def get_user_by_access_token(db: AsyncSession, token: str) -> User:
    """
        Ты мне токен, я тебе пользователя
    """
    user = await users_crud.get(db, decode_access_token(token))
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User by access token not found"
    )