from fastapi import Form
from pydantic import BaseModel


class AuthForm:
    email: str = Form(...)
    password: str = Form(...)


class TokensPair(BaseModel):
    """
        Модель, возвращаемая пользователю при входе или обновлении токенов
    """
    access_token: str
    token_type: str = "Bearer"
    expired_at: int # Время истечения срока действия токена в формате UNIX TIME
    refresh_token: str