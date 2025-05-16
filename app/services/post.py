from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import PostCategory
from app.models.post import Post
from app.models.post_media import PostMedia
from app.schemas.post import PostCreate, PostUpdate
from fastapi import UploadFile
from typing import List

from app.utils.file import save_upload_file


async def create_post_service(
        db: AsyncSession,
        post_data: PostCreate,
        author_id: int,
        media_files: List[UploadFile],
) -> Post:
    post = Post(
        title=post_data.title,
        content=post_data.content,
        visibility_type=post_data.visibility_type,
        is_published=post_data.is_published,
        author_id=author_id,
    )
    db.add(post)
    await db.flush()

    if post_data.category_ids:
        for cat_id in post_data.category_ids:
            db.add(PostCategory(post_id=post.id, category_id=cat_id))

    for i, media in enumerate(media_files):
        file_path = await save_upload_file(media, subdir="posts")
        db.add(PostMedia(post_id=post.id, file_path=file_path, order=i))

    await db.commit()
    await db.refresh(post)
    return post


async def update_post(
        db: AsyncSession, post: Post, update_data: PostUpdate
) -> Post:
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(post, field, value)

    if update_data.category_ids is not None:
        await db.execute(
            PostCategory.__table__.delete().where(PostCategory.post_id == post.id)
        )
        for cat_id in update_data.category_ids:
            db.add(PostCategory(post_id=post.id, category_id=cat_id))

    await db.commit()
    await db.refresh(post)
    return post


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()
