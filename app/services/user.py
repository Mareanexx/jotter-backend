from datetime import datetime

from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate


async def create_user(user_data: UserCreate, db: AsyncSession) -> Profile:
    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_data.email,
        password_hash=bcrypt.hash(user_data.password),
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        created_at=datetime.now()
    )
    db.add(user)
    await db.flush()

    profile = Profile(
        username=user_data.username,
        birthdate=user_data.birthdate,
        user_uuid=user.uuid,
        created_at=datetime.now()
    )
    db.add(profile)

    await db.commit()
    await db.refresh(user)
    return profile
