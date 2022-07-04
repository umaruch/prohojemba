from typing import Optional, Dict
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    id: int
    username: str
    avatar_uri: Optional[str] = None

    class Config:
        orm_mode=True

class UserOutput(BaseUser):
    pass


class CurrentUserOutput(BaseUser):
    email: EmailStr


class PatchUserForm:
    def __init__(self,
        username: Optional[str] = Form(None),
        avatar: Optional[UploadFile] = File(None)
    ) -> None:
        self.username = username
        self.avatar = avatar

    def fields(self) -> Dict:
        return {
            "username": self.username
        }