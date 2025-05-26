from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    read_time_seconds = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    profile_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    is_published = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="articles")
    collections = relationship("Collection", secondary="collection_articles", back_populates="articles")
