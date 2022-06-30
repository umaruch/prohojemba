from datetime import timedelta, datetime
import email
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


async def _encode_refresh_token(redis: Redis, user_id: int) -> str:
    token = secrets.token_hex(64)
    if await redis.get(token):
        return await _encode_refresh_token(redis, user_id)
    
    await redis.set(token, user_id, ex=5*60)
    return token


async def _decode_refresh_token(redis: Redis, token: str) -> int:
    try:
        return int(await redis.get(token))
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh_token"
        )


async def register_new_user(db: AsyncSession, redis: Redis, form: auth.SigninForm) -> auth.TokensPair:
    if await _validate_code(redis, form.email, form.code):
        user_id = await users_crud.create(db, 
            email=form.email, username=form.username,
            encoded_password=_get_password_hash(form.password)
        )

        return auth.TokensPair(
                access_token=_encode_access_token(user_id=user_id),
                refresh_token= await _encode_refresh_token(redis=redis, user_id=user_id))

    raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect validation code"
        )


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


async def update_tokens_pair(redis: Redis, token: str) -> auth.TokensPair:
    user_id = await _decode_refresh_token(redis, token)
    return auth.TokensPair(
            access_token=_encode_access_token(user_id=user_id),
            refresh_token= await _encode_refresh_token(redis=redis, user_id=user_id))
    

async def update_user_email(db: AsyncSession, redis: Redis, user_id: int, form: auth.UpdateEmailForm) -> None:
    if await _validate_code(redis, form.email, form.code):
        await users_crud.update(db, user_id, email=form.new_email)

    raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect validation code"
        )


async def update_user_password(db: AsyncSession, user_id: int, form: auth.UpdatePasswordForm) -> None:
    user = await users_crud.get_by_id(db, user_id)
    if user and _verify_password(form.current_password, user.encoded_password):
        await users_crud.update(db, user_id, 
            encoded_password=_get_password_hash(form.new_password))

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password")


async def restore_user_password(db: AsyncSession, redis: Redis, form: auth.RestorePasswordForm) -> None:
    if _validate_code(redis, form.email, form.code):
        user = await users_crud.get_by_email(db, form.email)
        await users_crud.update(db, user.id,
            encoded_password=_get_password_hash(form.new_password))

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Incorrect validation code"
    )


async def generate_validation_code(redis: Redis, email: str) -> str:
    code = secrets.token_hex(3)
    await redis.set(email, code, ex=5*60)
    return code


async def _validate_code(redis: Redis, email: str, code: str) -> bool:
    current_code = await redis.get(email)
    if current_code and code == current_code.decode("utf-8"):
        return True

    return False