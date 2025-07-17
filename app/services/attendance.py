from datetime import date, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import re

from app.models import Attendance, User
from app.schemas import AttendanceRecord, GetAttendanceReportRequest, AttendanceReportResponse


class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    def get_attendance_report(self, request: GetAttendanceReportRequest) -> AttendanceReportResponse:
        records = self.db.query(Attendance).filter(
            and_(
                Attendance.user_id == request.user_id,
                Attendance.date >= request.start_date,
                Attendance.date <= request.end_date
            )
        ).order_by(Attendance.date).all()

        attendance_records = []
        total_violations = 0.0

        for record in records:
            attendance_record = AttendanceRecord(
                date=record.date,
                time_in=record.time_in,
                time_out=record.time_out,
                leave=record.leave,
                violations=record.violations
            )
            attendance_records.append(attendance_record)
            total_violations += record.violations

        return AttendanceReportResponse(
            user_id=request.user_id,
            start_date=request.start_date,
            end_date=request.end_date,
            records=attendance_records,
            total_violations=total_violations,
            summary=""  # LLM will handle the formatting
        )

    def extract_date_range_from_query(self, query: str) -> Optional[tuple[date, date]]:
        date_patterns = [
            r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'(\d{1,2})-(\d{1,2})-(\d{4})'
        ]
        
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                if len(match) == 3:
                    if match[1].lower() in month_map:
                        day, month_name, year = match
                        month = month_map[month_name.lower()]
                    else:
                        day, month, year = match
                        month = int(month)
                    
                    try:
                        found_date = date(int(year), month, int(day))
                        dates.append(found_date)
                    except ValueError:
                        continue

        if len(dates) >= 2:
            dates.sort()
            return dates[0], dates[1]
        
        return None 