from typing import Dict, Any, Optional, Tuple
from datetime import timedelta, datetime
import random
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


