from sqlalchemy import Column, Integer, String


from src.models.base import Base


class Title(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    cover = Column(String, nullable=True)
    description = Column(String, nullable=True)
    year = Column(Integer)
