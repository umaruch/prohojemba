from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


from src.core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"])

oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.application.API_URL}/auth/token"
)
