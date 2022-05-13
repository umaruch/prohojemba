from typing import Optional


from src.schemes.base import ORMModel


class BaseProfile(ORMModel):
    username: str
    avatar: Optional[str]


class Profile(BaseProfile):
    """
        Вся информация о профиле пользователя
    """
    steam_id: Optional[str]
    playstation_id: Optional[str]
    switch_id: Optional[str]


class ProfilePreview(BaseProfile):
    """
        Базовая информация
    """
    pass