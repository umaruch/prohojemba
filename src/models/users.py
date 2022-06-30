from sqlalchemy import Column, Integer, String


from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True, unique=True)
    encoded_password = Column(String)
    username = Column(String, unique=True)
    avatar_uri = Column(String, nullable=True)