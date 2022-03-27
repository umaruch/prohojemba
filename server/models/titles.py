from sqlalchemy import Column, Integer, String

from server.core.db import Base


class Title(Base):
    __tablename__ = "titles"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(128))
    description = Column("description", String(1024))
    type = Column("type", String(16))
    release_year = Column("release_year", Integer)
    rating = Column("rating", Integer, nullable=True, default=None)
