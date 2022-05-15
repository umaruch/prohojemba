from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis
from datetime import datetime


from src.api import deps
from src.crud import users_crud, cache_crud
from src.models.users import User
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
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    user = await users_crud.get_user_by_email(db, form.email)
    if user and security.verify_password(form.password, user.password_hash):
        await users_crud.update_user(db, user, {
            "last_auth_at": datetime.utcnow()
        })

        access_token = security.encode_access_token(user.id)
        session_uuid, refresh_token = security.encode_refresh_token(user.id)

        await cache_crud.set_refresh_token(redis, refresh_token, user.id, session_uuid)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        } 
    
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")


@router.post("/token/update", tags=["Авторизация"])
async def update_tokens_pair(
    form: RefreshTokenForm = Depends(RefreshTokenForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
    ):
    """
        Проверка refresh токена, создание пары новых токенов

    """
    session_uuid, user_id = security.decode_refresh_token(form.refresh_token)

    if not form.refresh_token == await cache_crud.get_refresh_token(redis, user_id, session_uuid):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # TODO Добавить обновление последнего обновления токена
    await users_crud.update_user(db, user_id, {
            "last_auth_at": datetime.utcnow()
    })

    access_token = security.encode_access_token(user_id)
    session_uuid, refresh_token = security.encode_refresh_token(user_id, session_uuid)

    await cache_crud.set_refresh_token(redis, refresh_token, user_id, session_uuid)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/email/change", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def change_user_email(
    form: ChangeEmailForm = Depends(ChangeEmailForm),
    user: User = Depends(deps.get_current_user_by_access_token),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    if not await cache_crud.get_validation_code(redis, form.email, "emailchange") == form.code:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect email validation code")
    
    await users_crud.update_user(db, user, {
        "email": form.email
    })

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/password/change", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def change_user_password(
    form: ChangePasswordForm = Depends(ChangePasswordForm),
    user: User = Depends(deps.get_current_user_by_access_token),
    db: AsyncSession = Depends(deps.get_db_session)
):
    if not security.verify_password(form.current_password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect current password")
    
    await users_crud.update_user(db, user, {
        "password_hash": security.get_password_hash(form.new_password) 
    })

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/password/restore", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def restore_user_password(
    form: RestorePasswordForm = Depends(RestorePasswordForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    if not await cache_crud.get_validation_code(redis, form.email, "passrestore"):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect email validation code")

    user = await users_crud.get_user_by_email(db, form.email)
    await users_crud.update_user(db, user, {
        "password_hash": security.get_password_hash(form.password)
    }) 

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/email/validate", tags=["Авторизация"], status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def validate_email(
    tasks: BackgroundTasks,
    form: ValidateEmailForm = Depends(ValidateEmailForm),
    db: AsyncSession = Depends(deps.get_db_session),
    redis: Redis = Depends(deps.get_redis_connection)
):
    if form.validation_type == "signin":
        if await users_crud.get_user_by_email(db, form.email):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already exists")

    elif form.validation_type in ["passrestore", "emailchange"]:
        if not await users_crud.get_user_by_email(db, form.email):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User with email not found")
    
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid validation type")

    code = security.get_validation_code()
    await cache_crud.set_validation_code(redis, form.email, form.validation_type, code)

    tasks.add_task(email.send_register_message, email=form.email, code=code)

    return Response(status_code=status.HTTP_204_NO_CONTENT)