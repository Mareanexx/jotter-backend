from datetime import datetime
from pydantic import BaseModel


class ReportCreate(BaseModel):
    post_id: int


class ReportOut(BaseModel):
    id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True
