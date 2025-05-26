from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Collection(BaseModel):
    id: int
    name: str
    numberOfArticles: int = Field(..., alias="number_of_articles")
    createdAt: datetime = Field(..., alias="created_at")

    class Config:
        from_attributes = True
        populate_by_name = True


class ArticleImage(BaseModel):
    id: int
    photo: Optional[str]

    class Config:
        from_attributes = True


class CollectionWithArticleImages(BaseModel):
    collection: Collection
    previewPhotos: List[ArticleImage]


class NewCollectionRequest(BaseModel):
    name: str


class UpdateCollectionRequest(BaseModel):
    id: int
    name: str
