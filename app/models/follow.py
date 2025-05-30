from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Follow(Base):
    __tablename__ = "follows"
    follower_id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    following_id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
