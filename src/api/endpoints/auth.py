from urllib.request import Request
from fastapi import APIRouter, Form, Depends, status
from fastapi.responses import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis
from fastapi.security import OAuth2PasswordRequestForm

from src.api import deps
from src.schemes import auth
from src.services import security


router = APIRouter()


@router.post("/signin", tags=["Авторизация"])
async def signin(
    form: auth.SigninForm = Depends(auth.SigninForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
) -> None:
    await security.register_new_user(db, redis, form)


@router.post("/token", tags=["Авторизация"])
async def token(
    form: auth.LoginForm = Depends(auth.LoginForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    tokens_pair = await security.authenticate_user(db, redis, form)
    return tokens_pair


@router.post("/token/update", tags=["Авторизация"])
async def update_tokens_pair(
    refresh_token: str = Form(...)
):
    pass


@router.post("/email/change", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT)
async def change_user_email(
    new_email: EmailStr = Form(...),
    password: str = Form(...),
    code: str = Form(...)
):
    pass


@router.post("/password/change", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(
    current_password: str = Form(...),
    new_password: str = Form(...)
):
    pass


@router.post("/password/restore", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def restore_user_password(
    email: EmailStr = Form(...),
    code: str = Form(...)
):
    pass


@router.post("/validate", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT)
async def validate_email(
    email: EmailStr = Form(...),
    validation_type: str = Form(...),
    redis: Redis = Depends(deps.get_redis_connection)
):
    """
        Запрос на валидацию некоторых действий пользователя, 
        путем отправки кода на указанную почту
    """
    code = await security.generate_validation_code(redis, email)