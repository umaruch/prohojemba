from email.policy import default
from sqlalchemy import Column, Integer, String, ForeignKey

from src.models.base import Base


class Profile(Base):
    __tablename__ = "profiles"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    profile_id = Column("profile_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))

    username = Column("username", String(32), unique=True)
    avatar = Column("avatar", String(128), nullable=True)

    # Привязанные учетные записи
    steam_id = Column("steam_id", String(64), nullable=True, default=None)
    playstation_id = Column("playstation_id", String(64), nullable=True, default=None)
    switch_id = Column("switch_id", String(64), nullable=True, default=None)