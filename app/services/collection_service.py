from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.models.collection import Collection
from app.models.article import Article
from app.models.collections_articles import collection_articles
from app.models.profile import Profile
from app.schemas.article import CollectionArticle
from app.schemas.collections import NewCollectionRequest, UpdateCollectionRequest
from datetime import datetime


class CollectionService:
    @staticmethod
    async def create_collection(db: AsyncSession, request: NewCollectionRequest, profile: Profile):
        new_collection = Collection(
            name=request.name,
            number_of_articles=0,
            created_at=datetime.now(),
            profile_id=profile.id
        )
        db.add(new_collection)
        await db.commit()
        await db.refresh(new_collection)
        return new_collection

    @staticmethod
    async def get_all_collections(db: AsyncSession, profile: Profile):
        result = await db.execute(select(Collection).where(Collection.profile_id == profile.id).order_by(Collection.created_at.desc()))
        collections = result.scalars().all()

        # Получаем превью фото
        article_result = await db.execute(
            select(Collection.id, Article.id, Article.photo)
            .join(collection_articles, Collection.id == collection_articles.c.collection_id)
            .join(Article, Article.id == collection_articles.c.article_id)
            .where(Collection.profile_id == profile.id)
        )
        articles = article_result.fetchall()

        grouped = {}
        for collection_id, article_id, photo in articles:
            grouped.setdefault(collection_id, []).append({"id": article_id, "photo": photo})

        response = []
        for collection in collections:
            images = grouped.get(collection.id, [])[:3]  # максимум 3 превью
            response.append({
                "collection": collection,
                "previewPhotos": images
            })

        return response

    @staticmethod
    async def get_articles_by_collection_id(db: AsyncSession, collection_id: int) -> list[CollectionArticle]:
        result = await db.execute(
            select(Article, collection_articles.c.collection_id)
            .join(collection_articles, Article.id == collection_articles.c.article_id)
            .where(collection_id == collection_articles.c.collection_id)
        )
        rows = result.all()
        return [
            CollectionArticle(
                id=article.id,
                title=article.title,
                content=article.content,
                created_at=article.created_at,
                photo=article.photo,
                read_time_seconds=article.read_time_seconds,
                profile_id=article.profile_id,
                collection_id=collection_id
            )
            for article, _ in rows
        ]

    @staticmethod
    async def remove_article_from_collection(
            db: AsyncSession,
            collection_id: int,
            article_id: int
    ) -> None:
        stmt = delete(collection_articles).where(
            collection_id == collection_articles.c.collection_id,
            article_id == collection_articles.c.article_id
        )
        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def delete_collection(db: AsyncSession, collection_id: int):
        await db.execute(delete(Collection).where(Collection.id == collection_id))
        await db.commit()

    @staticmethod
    async def update_collection_name(db: AsyncSession, request: UpdateCollectionRequest):
        await db.execute(
            update(Collection)
            .where(Collection.id == request.id)
            .values(name=request.name)
        )
        await db.commit()
        result = await db.execute(select(Collection).where(Collection.id == request.id))
        return result.scalar_one()
