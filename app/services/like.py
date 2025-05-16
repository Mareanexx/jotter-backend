# services/like.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.like import Like
from sqlalchemy.future import select


async def toggle_like(db: AsyncSession, post_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(Like).where(Like.post_id == post_id, Like.author_id == user_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        await db.commit()
        return False
    else:
        like = Like(post_id=post_id, author_id=user_id)
        db.add(like)
        await db.commit()
        return True
