from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    post_id: int
    content: str
    parent_comment_id: Optional[int] = None


class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime
    parent_comment_id: Optional[int]
    replies: List["CommentOut"] = []

    class Config:
        from_attributes = True


CommentOut.model_rebuild()
