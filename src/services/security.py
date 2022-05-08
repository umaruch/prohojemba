from typing import Dict, Any
from datetime import timedelta, datetime
import jwt
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


from src.core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"])
oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.application.API_URL}/auth/token",
    scheme_name="AuthForm"
)
SECRET_KEY = settings.application.SECRET_KEY
ACCESS_TOKEN_LIFETIME = timedelta(hours=5)
REFRESH_TOKEN_LIFETIME = timedelta(days=3)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _encode_user_token(payload: Dict[str, Any]) -> str:
    """
    Генерация токена пользователя.
    scope может быть access_token|refresh_token
    """
    return jwt.encode(
        payload=payload,
        key=SECRET_KEY
    )


def encode_user_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "scope": "access_token",
        "exp": datetime.utcnow() + ACCESS_TOKEN_LIFETIME 
    }
    return _encode_user_token(payload)


def encode_user_refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "scope": "refresh_token",
        "exp": datetime.utcnow() + REFRESH_TOKEN_LIFETIME 
    }
    return _encode_user_token(payload)


def decode_user_token(token: str, scope: str) -> int:
    try:
        payload = jwt.decode()
        if payload["scope"] == scope:
            return scope["user_id"]
        raise HTTPException(status_code=401, detail='Invalid scope for token')

    # Вышел срок действия токена
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')
    
    # Скорее всего поддельный токен
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
