from sqlalchemy import Table, Column, ForeignKey

from app.core.database import Base

collection_articles = Table(
    "collection_articles",
    Base.metadata,
    Column("collection_id", ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True),
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)
)
