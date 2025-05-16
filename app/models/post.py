from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class PostVisibilityType(str, enum.Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    FOLLOWERS_ONLY = "Followers Only"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE"))
    title = Column(String(255))
    content = Column(Text)
    visibility_type = Column(String(15), nullable=False, default=PostVisibilityType.PUBLIC.value)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    is_published = Column(Boolean, default=False)

    author = relationship("Profile", back_populates="posts")
    media = relationship("PostMedia", back_populates="post", cascade="all, delete-orphan", lazy="selectin")
    categories = relationship(
        "Category",
        secondary="post_categories",
        back_populates="posts",  # Changed from "post" to "posts" to match Category model
        cascade="all, delete",
        lazy="selectin"
    )
