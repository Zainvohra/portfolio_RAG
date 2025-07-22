from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_, func

from app.models import Attendance
from app.schemas import (
    AttendanceRecord,
    GetAttendanceReportRequest,
    AttendanceReportResponse,
    AdminAttendanceRecord,
)


class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    def get_attendance_report(
        self, request: GetAttendanceReportRequest
    ) -> AttendanceReportResponse:
        records = (
            self.db.query(Attendance)
            .filter(
                and_(
                    Attendance.user_id == request.user_id,
                    Attendance.date >= request.start_date,
                    Attendance.date <= request.end_date,
                )
            )
            .order_by(Attendance.date)
            .all()
        )

        attendance_records = []
        total_violations = 0.0

        for record in records:
            attendance_record = AttendanceRecord(
                date=record.date,
                time_in=record.time_in,
                time_out=record.time_out,
                leave=record.leave,
                violations=record.violations,
            )
            attendance_records.append(attendance_record)
            total_violations += record.violations

        return AttendanceReportResponse(
            user_id=request.user_id,
            start_date=request.start_date,
            end_date=request.end_date,
            records=attendance_records,
            total_violations=total_violations,
            summary="",  # LLM will handle the formatting
        )

    def get_missing_attendance(self, request: GetAttendanceReportRequest) -> list:
        records = (
            self.db.query(Attendance)
            .filter(
                and_(
                    Attendance.user_id == request.user_id,
                    Attendance.date >= request.start_date,
                    Attendance.date <= request.end_date,
                    Attendance.leave.is_(None),
                    or_(
                        Attendance.time_in.is_(None),
                        Attendance.time_out.is_(None),
                    ),
                    # Exclude Saturday (6) and Sunday (0)
                    not_(func.extract("dow", Attendance.date).in_([0, 6])),
                )
            )
            .all()
        )

        attendance_records = []
        total_violations = 0.0

        for record in records:
            attendance_record = AttendanceRecord(
                date=record.date,
                time_in=record.time_in,
                time_out=record.time_out,
                leave=record.leave,
                violations=record.violations,
            )
            attendance_records.append(attendance_record)
            total_violations += record.violations

        return AttendanceReportResponse(
            user_id=request.user_id,
            start_date=request.start_date,
            end_date=request.end_date,
            records=attendance_records,
            total_violations=total_violations,
            summary="",
        )

    def _get_missing_attendance_user_ids(self, start_date: str, end_date: str):
        records = (
            self.db.query(Attendance)
            .filter(
                and_(
                    Attendance.date >= start_date,
                    Attendance.date <= end_date,
                    or_(
                        Attendance.violations > 1,
                        Attendance.leave.is_(None),
                    ),
                )
            )
            .all()
        )

        attendance_records = []

        for record in records:
            attendance_record = AdminAttendanceRecord(user_id=record.user_id)
            attendance_records.append(attendance_record)

        return attendance_records
