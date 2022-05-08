from fastapi import APIRouter, Form, Depends
from aioredis import Redis

from src.api import deps
from src.schemes.auth import AuthForm
from src.services import security

router = APIRouter()


@router.post("/signin", tags=["Авторизация"])
async def signin():
    return "Hello, World"


@router.post("/token", tags=["Авторизация"])
async def token():
    form: AuthForm = Depends(),
    access_token = security.encode_user_access_token(5)
    refresh_token = security.encode_user_refresh_token(5)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer" 
    }


@router.post("/token/update", tags=["Авторизация"])
async def update_tokens_pair(
    refresh_token: str = Form(...),
    redis_session: Redis = Depends(deps.get_redis_connection)
    ):
    """
        Проверка refresh токена, создание пары новых токенов

    """
    pass


@router.post("/email/change", tags=["Авторизация"])
async def chenge_user_email():
    pass


@router.post("/password/change", tags=["Авторизация"])
async def change_user_password():
    pass


@router.post("/password/restore", tags=["Авторизация"])
async def restore_user_password():
    pass


@router.post("/email/validate", tags=["Авторизация"])
async def validate_email():
    pass