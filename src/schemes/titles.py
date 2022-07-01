from typing import Optional
from pydantic import BaseModel


from src.core.constants import TitleTypes


class CreateTitleModel(BaseModel):
    """
        Класс для валидации полей формы создания файла
    """
    name: str
    type: str
    cover: Optional[str]
    description: Optional[str]
    year: str


class PatchTitleModel(BaseModel):
    """
        Класс для валидации полей формы редактирования тайтла
    """
    name: Optional[str]
    type: Optional[TitleTypes]
    cover: Optional[str]
    description: Optional[str]
    year: Optional[int]