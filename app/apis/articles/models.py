from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    url = Column(String)
    source = Column(String)
    publication_date = Column(DateTime(timezone=True), nullable=False)
    feed_id = Column(ForeignKey("feeds.id", ondelete="CASCADE"))

    feed = relationship("Feed", back_populates="articles")
