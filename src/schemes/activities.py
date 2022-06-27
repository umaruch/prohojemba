from pydantic import BaseModel
from datetime import date


from src.core.constants import ActivityStates


class CreateActivityModel(BaseModel):
    user_id: int
    title_id: int
    state: str
    updated_at: date = date.today()