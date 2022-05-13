from fastapi import Form
from pydantic import EmailStr


class SigninForm:
    """
        Форма, заполняемая при регистрации
    """
    def __init__(self,
        email: EmailStr = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        code: str = Form(..., regex=r"\d{6}")
    ) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.code = code


class LoginForm:
    """
        Форма, заполняемая для получения токена пользователя
    """
    pass


class RefreshTokenForm:
    pass


class ValidateEmailForm:
    def __init__(self,
        email: EmailStr = Form(...),
        validation_type: str = Form(...)
    ) -> None:
        self.email = email
        self.validation_type = validation_type