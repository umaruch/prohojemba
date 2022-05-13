from pydantic import BaseModel


class ORMModel(BaseModel):
    """
    Для отправки данных клиенту
    """
    class Config:
        orm_mode = True