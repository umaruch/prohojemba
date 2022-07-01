from sqlalchemy import Column, Integer, ForeignKey, String, Date, UniqueConstraint

from src.models.base import Base


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"))
    title_id = Column(Integer, ForeignKey("titles.id", ondelete="cascade"))
    state = Column(String)
    updated_at = Column(Date)

    __table_args__ = (
        UniqueConstraint("user_id", "title_id", name="u_user_title"),
    )