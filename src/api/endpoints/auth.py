from fastapi import APIRouter, Form, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis

from src.api import deps
from src.crud import users_crud, cache_crud
from src.schemes.auth import TokensPair
from src.schemes.forms import SigninForm, LoginForm, RefreshTokenForm, ValidateEmailForm, ChangeEmailForm, ChangePasswordForm, RestorePasswordForm
from src.services import security, email

router = APIRouter()


@router.post("/signin", tags=["Авторизация"], response_model=TokensPair)
async def signin(
    form: SigninForm = Depends(SigninForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
) -> TokensPair:
    # Проверка валидности email
    if not await cache_crud.get_validation_code(redis, form.email, "signin") == form.code:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect email validation code")

    # Проверка наличия пользователя с тем-же именем
    if await users_crud.get_profile_by_username(db, form.username):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already exists")

    # Создание пользователя 
    user_id = await users_crud.create_user(db, form.email, security.get_password_hash(form.password), form.username)

    access_token = security.encode_access_token(user_id)
    session_uuid, refresh_token = security.encode_refresh_token(user_id)

    await cache_crud.set_refresh_token(redis, refresh_token, user_id, session_uuid)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/token", tags=["Авторизация"], response_model=TokensPair)
async def token(
    form: LoginForm = Depends(LoginForm),
    redis: Redis = Depends(deps.get_redis_connection)
):
    access_token = security.encode_access_token(user_id)
    session_uuid, refresh_token = security.encode_refresh_token(user_id)

    await cache_crud.set_refresh_token(redis, refresh_token, user_id, session_uuid)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/token/update", tags=["Авторизация"])
async def update_tokens_pair(
    form: RefreshTokenForm = Depends(RefreshTokenForm),
    redis: Redis = Depends(deps.get_redis_connection)
    ):
    """
        Проверка refresh токена, создание пары новых токенов

    """
    session_uuid, user_id = security.decode_refresh_token(form.refresh_token)

    if not form.refresh_token == await cache_crud.get_refresh_token(redis, user_id, session_uuid):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    access_token = security.encode_access_token(user_id)
    session_uuid, refresh_token = security.encode_refresh_token(user_id, session_uuid)

    await cache_crud.set_refresh_token(redis, refresh_token, user_id, session_uuid)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/email/change", tags=["Авторизация"])
async def chenge_user_email(
    form: ChangeEmailForm = Depends(ChangeEmailForm)
):
    pass


@router.post("/password/change", tags=["Авторизация"])
async def change_user_password(
    form: ChangePasswordForm = Depends(ChangePasswordForm)
):
    pass


@router.post("/password/restore", tags=["Авторизация"])
async def restore_user_password(
    form: RestorePasswordForm = Depends(RestorePasswordForm)
):
    pass


@router.post("/email/validate", tags=["Авторизация"])
async def validate_email(
    tasks: BackgroundTasks,
    form: ValidateEmailForm = Depends(ValidateEmailForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    code = security.get_validation_code()
    if await users_crud.get_user_by_email(db, form.email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already exists")

    await cache_crud.set_validation_code(redis, form.email, form.validation_type, code)

    tasks.add_task(email.send_register_message, email=form.email, code=code)

    return {"status": "ok"}