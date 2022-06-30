from datetime import timedelta, datetime
import secrets 
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


def _decode_access_token(token: str) -> int:
    pass


async def _encode_refresh_token(redis: Redis, user_id: int) -> str:
    token = secrets.token_hex(64)
    if await redis.get(token):
        return await _encode_refresh_token(redis, user_id)
    
    await redis.set(token, user_id, ex=60)
    return token


def _decode_refresh_token(redis: Redis, token: str) -> str:
    pass


async def register_new_user(db: AsyncSession, redis: Redis, form: auth.SigninForm) -> auth.TokensPair:
    if not await _validate_code(redis, form.email, form.code):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неверный код валидации"
        )
    
    user = await users_crud.create(db, 
        email=form.email, username=form.username,
        encoded_password=_get_password_hash(form.password)
    )

    return auth.TokensPair(
            access_token=_encode_access_token(user_id=user.id),
            refresh_token= await _encode_refresh_token(redis=redis, user_id=user.id))


async def authenticate_user(db: AsyncSession, redis: Redis, form: auth.LoginForm) -> auth.TokensPair:
    user = await users_crud.get_by_email(db, form.email)
    if user and _verify_password(form.password, user.encoded_password):
        return auth.TokensPair(
            access_token=_encode_access_token(user_id=user.id),
            refresh_token= await _encode_refresh_token(redis=redis, user_id=user.id))

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )


async def get_user_by_access_token(db: AsyncSession, token: str) -> User:
    """
        Ты мне токен, я тебе пользователя
    """
    user = await users_crud.get(db, _decode_access_token(token))
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User by access token not found"
    )


async def update_tokens_pair(redis: Redis, token: str) -> auth.TokensPair:
    pass


async def generate_validation_code(redis: Redis, email: str) -> str:
    code = secrets.token_hex(3)
    await redis.set(email, code, ex=5*60)
    return code


async def _validate_code(redis: Redis, email: str, code: str) -> bool:
    current_code = await redis.get(email)
    if current_code and code == current_code.decode("utf-8"):
        return True

    return False