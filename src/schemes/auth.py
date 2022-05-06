from pydantic import BaseModel


class TokensPair(BaseModel):
    """
        Модель, возвращаемая пользователю при входе или обновлении токенов
    """
    access_token: str
    token_type: str = "Bearer"
    expired_at: int # Время истечения срока действия токена в формате UNIX TIME
    refresh_token: str