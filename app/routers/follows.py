# controllers/follow.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.follows import toggle_follow
from app.core.auth import get_current_profile
from app.models.profile import Profile

router = APIRouter(prefix="/follows", tags=["Follows"])


@router.post("/{user_id}")
async def follow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Profile = Depends(get_current_profile),
):
    if current_user.id == user_id:
        return {"error": "Cannot follow yourself"}
    followed = await toggle_follow(db, current_user.id, user_id)
    return {"followed": followed}
