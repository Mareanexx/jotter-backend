from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.report import Report
from app.models.post import Post
from app.schemas.report import ReportCreate
from fastapi import HTTPException, status


async def create_report(db: AsyncSession, report_in: ReportCreate) -> Report:
    post_result = await db.execute(select(Post).where(Post.id == report_in.post_id))
    post = post_result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    report = Report(post_id=report_in.post_id)
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def get_reports_for_post(db: AsyncSession, post_id: int) -> list[Report]:
    result = await db.execute(select(Report).where(Report.post_id == post_id).order_by(Report.created_at))
    return list(result.scalars().all())
