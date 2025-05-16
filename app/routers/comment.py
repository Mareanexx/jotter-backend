# controllers/comment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.comment import CommentCreate, CommentOut
from app.services import comment as comment_service
from app.core.auth import get_current_profile
from app.models.profile import Profile
from typing import List

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentOut)
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Profile = Depends(get_current_profile),
):
    return await comment_service.create_comment(db, comment_in, current_user.id)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Profile = Depends(get_current_profile),
):
    success = await comment_service.delete_comment(db, comment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")


@router.get("/post/{post_id}", response_model=List[CommentOut])
async def get_comments_for_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await comment_service.get_comments_for_post(db, post_id)
