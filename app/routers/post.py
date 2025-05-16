# controllers/post.py
from fastapi import APIRouter, Depends, UploadFile, File, Form
import json
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.post import PostRead, PostCreate
from app.services.post import create_post_service
from app.core.database import get_db
from app.models.profile import Profile
from app.core.auth import get_current_profile

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostRead)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    visibility_type: str = Form(...),
    is_published: bool = Form(True),
    category_ids: str = Form("[]"),
    media: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db),
    current_user: Profile = Depends(get_current_profile),
):
    category_ids = json.loads(category_ids)
    post_data = PostCreate(
        title=title,
        content=content,
        visibility_type=visibility_type,
        is_published=is_published,
        category_ids=category_ids,
    )
    post = await create_post_service(
        db=db, post_data=post_data, author_id=current_user.id, media_files=media
    )
    return post
