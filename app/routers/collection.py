from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_inspection.typing_objects import alias

from app.core.database import get_db
from app.models.article import Article
from app.schemas.article import CollectionArticle
from app.schemas.collections import *
from app.services.collection_service import CollectionService
from app.core.auth import get_current_profile
from app.core.wrapped_response import WrappedResponse

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.post("", response_model=WrappedResponse[Collection])
async def add_collection(
    request: NewCollectionRequest,
    db: AsyncSession = Depends(get_db),
    profile = Depends(get_current_profile)
):
    collection = await CollectionService.create_collection(db, request, profile)
    return WrappedResponse(message="Collection created", data=collection)


@router.get("", response_model=WrappedResponse[List[CollectionWithArticleImages]])
async def get_all_collections(
    db: AsyncSession = Depends(get_db),
    profile = Depends(get_current_profile)
):
    collections = await CollectionService.get_all_collections(db, profile)
    return WrappedResponse(data=collections)


@router.get("/{collection_id}", response_model=WrappedResponse[List[CollectionArticle]])
async def get_articles_by_collection_id(
    collection_id: int,
    db: AsyncSession = Depends(get_db)
):
    articles = await CollectionService.get_articles_by_collection_id(db, collection_id)
    return WrappedResponse(data=articles)


@router.delete("/{collection_id}", response_model=WrappedResponse[None])
async def delete_collection_by_id(
    collection_id: int,
    db: AsyncSession = Depends(get_db)
):
    await CollectionService.delete_collection(db, collection_id)
    return WrappedResponse(message="Collection deleted")

@router.delete("")
async def remove_article_from_collection(
    collection_id: int,
    article_id: int,
    db: AsyncSession = Depends(get_db)
):
    await CollectionService.remove_article_from_collection(db, collection_id, article_id)
    return WrappedResponse(data=None)

@router.patch("", response_model=WrappedResponse[Collection])
async def update_collection(
    request: UpdateCollectionRequest,
    db: AsyncSession = Depends(get_db)
):
    updated = await CollectionService.update_collection_name(db, request)
    return WrappedResponse(message="Collection updated", data=updated)
