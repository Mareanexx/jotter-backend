from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    posts = relationship(
        "Post",
        secondary="post_categories",
        back_populates="categories"
    )


class PostCategory(Base):
    __tablename__ = "post_categories"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"), primary_key=True)
