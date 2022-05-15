import email
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
        Форма, заполняемая для получения токенов авторизации
    """
    def __init__(self,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ) -> None:
        self.email = email
        self.password = password


class RefreshTokenForm:
    def __init__(self,
        refresh_token: str = Form(...)
    ) -> None:
        self.refresh_token = refresh_token


class ValidateEmailForm:
    def __init__(self,
        email: EmailStr = Form(...),
        validation_type: str = Form(...)
    ) -> None:
        self.email = email
        self.validation_type = validation_type


class ChangeEmailForm:
    def __init__(self,
        email: EmailStr = Form(...),
        password: str = Form(...),
        code: str = Form(...)
    ) -> None:
        self.email = email
        self.password = password
        self.code = code


class ChangePasswordForm:
    def __init__(self,
        current_password: str = Form(...),
        new_password: str = Form(...)
    ) -> None:
        self.current_password = current_password
        self.new_password = new_password


class RestorePasswordForm(ChangeEmailForm):
    pass
