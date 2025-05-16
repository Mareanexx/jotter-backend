from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import Form
from pydantic import BaseModel, Field


class PostVisibilityType(str, Enum):
    PRIVATE = "Private"
    PUBLIC = "Public"
    FOLLOWERS_ONLY = "Followers Only"


# ============ CATEGORY ============

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ============ POST MEDIA ============

class PostMediaRead(BaseModel):
    id: int
    file_path: str
    order: int

    class Config:
        from_attributes = True


# ============ POST ============

class PostBase(BaseModel):
    title: str
    content: str
    visibility_type: PostVisibilityType
    is_published: Optional[bool] = True


class PostCreate(PostBase):
    category_ids: Optional[List[int]] = Field(default=[])


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    visibility_type: Optional[PostVisibilityType]
    is_published: Optional[bool]
    category_ids: Optional[List[int]] = None


class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    media: List[PostMediaRead] = []
    categories: List[CategoryRead] = []

    class Config:
        from_attributes = True
