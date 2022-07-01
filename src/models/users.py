from email.policy import default
from sqlalchemy import Column, Integer, String, Boolean


from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True, unique=True)
    encoded_password = Column(String)
    username = Column(String, unique=True)
    avatar_uri = Column(String, nullable=True)