from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.like import toggle_like
from app.core.auth import get_current_profile
from app.models.profile import Profile

router = APIRouter(prefix="/posts", tags=["Likes"])


@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Profile = Depends(get_current_profile),
):
    liked = await toggle_like(db, post_id, current_user.id)
    return {"liked": liked}
