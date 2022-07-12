from typing import List
from unittest.mock import Base
from pydantic import BaseModel
from datetime import date


from src.schemes.base import ORMModel
from src.schemes.titles_schemes import TitlePreview
from src.core.constants import ActivityStates


class BaseActivity(ORMModel):
    id: int
    state: ActivityStates
    updated_at: date


class ActivityPreview(BaseActivity):
    title: TitlePreview
