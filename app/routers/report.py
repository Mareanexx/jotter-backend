from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.report import ReportCreate, ReportOut
from app.services.report import create_report, get_reports_for_post

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", response_model=ReportOut)
async def create_report(report_in: ReportCreate, db: AsyncSession = Depends(get_db)):
    return await create_report(db, report_in)


@router.get("/post/{post_id}", response_model=list[ReportOut])
async def get_reports_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_reports_for_post(db, post_id)
