from fastapi import APIRouter, Form, status
from fastapi.responses import Response
from pydantic import EmailStr


router = APIRouter()


@router.post("/signin", tags=["Авторизация"])
async def signin(
    email: EmailStr = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    code: str = Form(...)
) -> None:
    """
        Регистрация нового пользователя
        1) Проверка кода негистрации
        2) Создание хэша пароля
        3) Создание записи о новом пользователе
        4) Генерация токенов доступа
        5)
    """
    pass


@router.post("/token", tags=["Авторизация"])
async def token(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    pass


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
    validation_type: str = Form(...) 
):
    """
        Запрос на валидацию некоторых действий пользователя, 
        путем отправки кода на указанную почту
    """
    pass