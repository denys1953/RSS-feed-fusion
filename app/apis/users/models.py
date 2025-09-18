from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

subscription_table = Table(
    "subscription_users_to_feeds",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("feed_id", Integer, ForeignKey("feeds.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    feeds = relationship(
        "Feed",
        secondary=subscription_table,
        back_populates="subscribers"
    )

