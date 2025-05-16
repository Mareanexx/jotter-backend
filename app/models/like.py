# models/like.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Like(Base):
    __tablename__ = "likes"
    author_id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
