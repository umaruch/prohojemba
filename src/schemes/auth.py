from fastapi import Form
from pydantic import BaseModel, EmailStr


from src.core.constants import ValidationTypes


class SigninForm:
    def __init__(self,
        email: EmailStr = Form(...),
        password: str = Form(...),
        username: str = Form(...),
        code: str = Form(...)
    ) -> None:
        self.email = email
        self.password = password
        self.username = username
        self.code = code


class LoginForm:
    def __init__(self,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ) -> None:
        self.email = email
        self.password = password


class UpdateEmailForm:
    def __init__(self,
        new_email: EmailStr = Form(...),
        password: str = Form(...),
        code: str = Form(...)
    ) -> None:
        self.new_email = new_email
        self.password = password
        self.code = code


class UpdatePasswordForm:
    def __init__(self,
        current_password: str = Form(...),
        new_password: str = Form(...)
    ) -> None:
        self.current_password = current_password
        self.new_password = new_password


class RestorePasswordForm:
    def __init__(self,
        email: EmailStr = Form(...),
        new_password: str = Form(...),
        code: str = Form(...)
    ) -> None:
        self.email = email
        self.new_password = new_password
        self.code = code


class ValidationRequestForm:
    def __init__(self,
        email: EmailStr = Form(...),
        validation_type: ValidationTypes = Form(...)
    ) -> None:
        self.email = email
        self.validation_type = validation_type


class TokensPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"