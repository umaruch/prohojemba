from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship


from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    
    email = Column("email", String(32), unique=True, index=True)
    password_hash = Column("password_hash", String(256))
    joined_at = Column("joined_at", Date)
    last_auth_at = Column("last_auth_at", DateTime)

    profile = relationship("Profile", uselist=False)
