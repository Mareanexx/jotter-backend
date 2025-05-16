from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate
from datetime import datetime


async def create_profile(profile_data: ProfileCreate, db: AsyncSession):
    profile = Profile(
        **profile_data.model_dump(),
        created_at=datetime.now()
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_profile_by_username(username: str, db: AsyncSession):
    result = await db.execute(select(Profile).where(Profile.username == username))
    return result.scalar_one_or_none()
