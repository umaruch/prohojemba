from typing import Optional, Dict
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, EmailStr


from src.schemes.base import ORMModel


class UserOutput(ORMModel):
    id: int
    username: str
    avatar_uri: Optional[str] = None


class CurrentUserOutput(UserOutput):
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