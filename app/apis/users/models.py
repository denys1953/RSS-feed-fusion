from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

from app.db.association_tables import subscription_table

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
        lazy="selectin",
        back_populates="subscribers"
    )

