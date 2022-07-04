from fastapi import APIRouter, Form, Depends, BackgroundTasks, status
from fastapi.responses import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis
from fastapi.security import OAuth2PasswordRequestForm

from src.api import deps
from src.schemes import auth
from src.services import security, email


router = APIRouter()


@router.post("/signin", tags=["Авторизация"], response_model=auth.TokensPair)
async def signin(
    form: auth.SigninForm = Depends(auth.SigninForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
) -> None:
    return await security.register_new_user(db, redis, form)


@router.post("/token", tags=["Авторизация"], response_model=auth.TokensPair)
async def token(
    form: auth.LoginForm = Depends(auth.LoginForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    return await security.authenticate_user(db, redis, form)


@router.post("/token/update", tags=["Авторизация"], response_model=auth.TokensPair)
async def update_tokens_pair(
    refresh_token: str = Form(...),
    redis: Redis = Depends(deps.get_redis_connection)
):
    return await security.update_tokens_pair(redis, refresh_token)


@router.post("/email/change", tags=["Авторизация"], 
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def change_user_email(
    current_user_id: int = Depends(deps.get_current_user_id),
    form: auth.UpdateEmailForm = Depends(auth.UpdateEmailForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    await security.update_user_email(db, redis, current_user_id, form)


@router.post("/password/change", tags=["Авторизация"], 
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def change_user_password(
    current_user_id: int = Depends(deps.get_current_user_id),
    form: auth.UpdatePasswordForm = Depends(auth.UpdatePasswordForm),
    db: AsyncSession = Depends(deps.get_db_session)
):
    await security.update_user_password(db, current_user_id, form)


@router.post("/password/restore", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def restore_user_password(
    form: auth.RestorePasswordForm = Depends(auth.RestorePasswordForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    await security.restore_user_password(db, redis, form)


@router.post("/validate", tags=["Авторизация"], 
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def validate_email(
    tasks: BackgroundTasks,
    form: auth.ValidationRequestForm = Depends(auth.ValidationRequestForm),
    redis: Redis = Depends(deps.get_redis_connection)
):
    """
        Запрос на валидацию некоторых действий пользователя, 
        путем отправки кода на указанную почту
    """
    code = await security.generate_validation_code(redis, form.email)
    tasks.add_task(email.send_validation_email, form.email, code)