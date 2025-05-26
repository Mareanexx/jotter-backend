from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CollectionArticle(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    photo: Optional[str]
    read_time_seconds: Optional[int]
    profile_id: int
    collection_id: int

    class Config:
        from_attributes = True
