from typing import Dict, Any, Optional, Tuple
from datetime import timedelta, datetime
import jwt
import uuid
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext


from src.core.settings import settings


SECRET_KEY = settings.application.SECRET_KEY
ACCESS_TOKEN_LIFETIME = timedelta(seconds=settings.application.ACCESS_TOKEN_EXPIRE_SECONDS)
REFRESH_TOKEN_LIFETIME = timedelta(seconds=settings.application.REFRESH_TOKEN_EXPIRE_SECONDS)


pwd_context = CryptContext(schemes=["bcrypt"])
bearer = HTTPBearer()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _encode_token(payload: Dict[str, Any]) -> str:
    """
    Генерация токена пользователя.
    scope может быть access_token|refresh_token
    """
    return jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm="HS256"
    )


def _create_session_uuid() -> str:
    return uuid.uuid4().hex


def encode_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "scope": "access_token",
        "exp": datetime.utcnow() + ACCESS_TOKEN_LIFETIME 
    }
    return _encode_token(payload)


def encode_refresh_token(user_id: int, session_uuid: Optional[str] = None) -> Tuple[str, str]:
    """
    return: session_uuid, refresh_token
    """
    if not session_uuid:
        session_uuid = _create_session_uuid()

    payload = {
        "user_id": user_id,
        "session_uuid": session_uuid,
        "scope": "refresh_token",
        "exp": datetime.utcnow() + REFRESH_TOKEN_LIFETIME 
    }
    return session_uuid, _encode_token(payload)
 

def _decode_user_token(token: str, scope: str) -> Dict[str, str]:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        if payload["scope"] == scope:
            return payload
        raise HTTPException(status_code=401, detail='Token scope invalid')

    # Вышел срок действия токена
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    
    # Скорее всего поддельный токен
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def decode_access_token(token: str) -> int:
    payload = _decode_user_token(token, "access_token")
    return int(payload["user_id"])


def decode_refresh_token(token: str) -> Tuple[int, str]:
    """
    return: session_uuid, user_id
    """
    payload = _decode_user_token(token, "refresh_token")
    return payload["session_uuid"], int(payload["user_id"])
    

    