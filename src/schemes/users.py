
from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class PatchUser(BaseModel):
    """
        Модель валидации данных для редактирования пользователя
    """
    