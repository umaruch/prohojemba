from typing import Optional, List
from pydantic import BaseModel

from src.schemes.base import ORMModel
from src.core.constants import TitleTypes


class TitlePreview(ORMModel):
    id: int
    name: str
    type: TitleTypes
    cover: str
    year: str


class TitlesList(BaseModel):
    items: List[TitlePreview]


class TitleFullInfo(TitlePreview):
    description: str