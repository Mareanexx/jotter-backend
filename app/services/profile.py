from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import UpdateProfileRequest


async def get_profile_by_user_uuid(user_uuid: UUID, db: AsyncSession) -> Optional[Profile]:
    stmt = (
        select(Profile)
        .options(joinedload(Profile.user))
        .where(Profile.user_uuid == user_uuid)
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_profile(data: UpdateProfileRequest, avatar_url: Optional[str], db: AsyncSession):
    result = await db.execute(
        select(Profile)
        .options(joinedload(Profile.user))
        .where(Profile.id == data.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        return None

    if data.username is not None:
        profile.username = data.username
    if data.bio is not None:
        profile.bio = data.bio
    if data.birthdate is not None:
        profile.birthdate = data.birthdate
    if avatar_url is not None:
        profile.avatar = avatar_url
    if data.email is not None:
        user = await db.get(User, profile.user_uuid)
        if user:
            user.email = data.email

    await db.commit()
    await db.refresh(profile)
    return profile
