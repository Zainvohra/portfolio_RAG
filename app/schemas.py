from pydantic import BaseModel, Field
from datetime import date, time
from typing import List, Optional


class PulseAIPayload(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000)


class AttendanceRecord(BaseModel):
    date: date
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    leave: Optional[str] = None
    violations: float = 0.0

    class Config:
        from_attributes = True


class AdminAttendanceRecord(BaseModel):
    user_id: int


class GetAttendanceReportRequest(BaseModel):
    user_id: int
    start_date: date
    end_date: date


class AttendanceReportResponse(BaseModel):
    user_id: int | None
    start_date: date
    end_date: date
    records: List[AttendanceRecord]
    total_violations: float
    summary: str
