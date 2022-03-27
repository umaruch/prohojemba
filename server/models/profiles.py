from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey

from server.core.db import Base


class Profile(Base):
    __tablename__ = "profiles"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        unique=True)
    username = Column("username", String(32), unique=True)
    avatar = Column("avatar", String(128), nullable=True)

