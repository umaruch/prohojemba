from typing import Dict, Any
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


from src.core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"])
oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.application.API_URL}/auth/token"
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def encode_token(payload: Dict[str, Any]) -> str:
    pass


def decode_token(token: str) -> Dict[str, Any]:
    pass

