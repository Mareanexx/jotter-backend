import json
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.wrapped_response import WrappedResponse
from app.schemas.profile import ProfileCreate, ProfileOut, UpdateProfileRequest
from app.services.profile import get_profile_by_user_uuid, update_profile
from app.utils.file import save_upload_file

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=WrappedResponse[ProfileOut])
async def get_profile(userUuid: UUID, db: AsyncSession = Depends(get_db)):
    profile = await get_profile_by_user_uuid(userUuid, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return WrappedResponse(
        data=ProfileOut(
            id=profile.id,
            username=profile.username,
            bio=profile.bio,
            birthdate=profile.birthdate,
            avatar=profile.avatar,
            user_uuid=profile.user_uuid,
            created_at=profile.created_at,
            email=profile.user.email
        )
    )


@router.patch("/", response_model=WrappedResponse[ProfileOut])
async def patch_profile(
        data: str = Form(...),
        avatar: Optional[UploadFile] = File(None),
        db: AsyncSession = Depends(get_db)
):
    try:
        update_data = UpdateProfileRequest(**json.loads(data))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid data format")

    avatar_url = None
    if avatar:
        avatar_url = await save_upload_file(avatar, subdir="avatars")

    profile = await update_profile(update_data, avatar_url, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return WrappedResponse(
        data=ProfileOut(
            id=profile.id,
            username=profile.username,
            bio=profile.bio,
            birthdate=profile.birthdate,
            avatar=profile.avatar,
            user_uuid=profile.user_uuid,
            created_at=profile.created_at,
            email=profile.user.email
        )
    )
