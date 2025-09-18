from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, DateTime, func, null
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.apis.users.models import subscription_table

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, default="Untitled Feed")
    url = Column(String, unique=True)
    last_fetched_at = Column(DateTime)
    subscribers = relationship(
        "User",
        secondary=subscription_table,
        back_populates="feeds"
    )

