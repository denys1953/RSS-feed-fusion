from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    url = Column(String)
    publication_date = Column(DateTime)
    feed_id = Column(ForeignKey("feeds.id"))