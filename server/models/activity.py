from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from server.core.db import Base


class Activity(Base):
    __tablename__ = "activity"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", uselist=False)

    title_id = Column("title_id", Integer, ForeignKey("titles.id", ondelete="CASCADE"))
    title = relationship("Title", uselist=False)

    state = Column("state", String(16))
    updated_at = Column("updated_at", DateTime)

    # Коомбинация user и title должна быть уникальной
    __table_args__ = (UniqueConstraint("user_id", "title_id", name="activity_user_title_uc"),)