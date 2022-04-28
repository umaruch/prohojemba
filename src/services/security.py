from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])

