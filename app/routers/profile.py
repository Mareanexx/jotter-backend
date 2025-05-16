from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.profile import ProfileCreate, ProfileOut
from app.services.profile import create_profile, get_profile_by_username

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=ProfileOut)
async def create(profile_data: ProfileCreate, db: AsyncSession = Depends(get_db)):
    return await create_profile(profile_data, db)


@router.get("/{username}", response_model=ProfileOut)
async def get(username: str, db: AsyncSession = Depends(get_db)):
    profile = await get_profile_by_username(username, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
