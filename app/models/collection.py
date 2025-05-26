from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    number_of_articles = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    profile_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    articles = relationship("Article", secondary="collection_articles", back_populates="collections")
