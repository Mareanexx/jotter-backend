from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.follow import Follow


async def toggle_follow(db: AsyncSession, follower_id: int, following_id: int) -> bool:
    result = await db.execute(
        select(Follow).where(
            Follow.follower_id == follower_id, Follow.following_id == following_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        await db.delete(existing)
        await db.commit()
        return False
    else:
        follow = Follow(follower_id=follower_id, following_id=following_id)
        db.add(follow)
        await db.commit()
        return True
