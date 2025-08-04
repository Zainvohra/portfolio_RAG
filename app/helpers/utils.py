# app/services/mcp_helpers.py
"""
Helper Functions
This module contains all the helper functions that can be used by MCP tools or function tools
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from datetime import date


from app.services.attendance import AttendanceService
from app.schemas import GetAttendanceReportRequest
from app.database import SessionLocal
from app.services.onboarding_email import OnboardingEmailService


def _get_attendance_report_logic(user_id: int, start_date: str, end_date: str) -> str:
    """Helper function to get attendance report logic"""
    try:
        print(
            f"Getting attendance report for user {user_id} from {start_date} to {end_date}"
        )
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        db = SessionLocal()
        try:
            attendance_service = AttendanceService(db)
            request = GetAttendanceReportRequest(
                user_id=user_id, start_date=start, end_date=end
            )
            report = attendance_service.get_attendance_report(request)
            result = json.dumps(
                {
                    "user_id": report.user_id,
                    "start_date": report.start_date.isoformat(),
                    "end_date": report.end_date.isoformat(),
                    "total_violations": report.total_violations,
                    "records": [
                        {
                            "date": record.date.isoformat(),
                            "time_in": (
                                record.time_in.isoformat() if record.time_in else None
                            ),
                            "time_out": (
                                record.time_out.isoformat() if record.time_out else None
                            ),
                            "leave": record.leave,
                            "violations": record.violations,
                        }
                        for record in report.records
                    ],
                }
            )
            print(f"Successfully generated report with {len(report.records)} records")
            return result
        finally:
            db.close()
    except Exception as e:
        print(f"Error in _get_attendance_report_logic: {str(e)}")
        return f"Error generating attendance report: {str(e)}"


def _get_missing_attendance_user_ids(start_date: str, end_date: str) -> str:
    """Helper function to get missing attendance user IDs"""
    try:
        print(f"Getting admin attendance report from {start_date} to {end_date}")
        db = SessionLocal()
        try:
            attendance_service = AttendanceService(db)
            missing_records = attendance_service._get_missing_attendance_user_ids(
                start_date, end_date
            )
            unique_user_ids = set(record.user_id for record in missing_records)
            result = json.dumps([{"user_id": id} for id in unique_user_ids])
            print(
                f"Successfully generated admin report with {len(unique_user_ids)} records"
            )
            return result
        finally:
            db.close()
    except Exception as e:
        print(f"Error in _get_admin_attendance_report_logic: {str(e)}")
        return f"Error generating admin attendance report: {str(e)}"


def _get_missing_attendance(user_id: int, start_date: str, end_date: str) -> str:
    """Helper function to get missing attendance for a specific user"""
    try:
        print(
            f"Getting missing attendance for user {user_id} from {start_date} to {end_date}"
        )
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        db = SessionLocal()
        try:
            attendance_service = AttendanceService(db)
            request = GetAttendanceReportRequest(
                user_id=user_id, start_date=start, end_date=end
            )
            report = attendance_service.get_missing_attendance(request)
            result = json.dumps(
                {
                    "user_id": user_id,
                    "start_date": report.start_date.isoformat(),
                    "end_date": report.end_date.isoformat(),
                    "total_violations": report.total_violations,
                    "records": [
                        {
                            "date": record.date.isoformat(),
                            "time_in": (
                                record.time_in.isoformat() if record.time_in else None
                            ),
                            "time_out": (
                                record.time_out.isoformat() if record.time_out else None
                            ),
                            "leave": record.leave,
                        }
                        for record in report.records
                    ],
                }
            )
            print(f"Successfully generated report with {len(report.records)} records")
            return result
        finally:
            db.close()
    except Exception as e:
        print(f"Error in _get_attendance_report_logic: {str(e)}")
        return f"Error generating attendance report: {str(e)}"


async def _send_onboarding_email(user_id: int) -> str:
    """Helper function to send onboarding email"""
    try:
        print(f"Sending onboarding email to user {user_id}")
        db = SessionLocal()
        try:
            service = OnboardingEmailService(db)
            result = await service.send_onboarding_email_to_user(user_id)
            return result
        finally:
            db.close()
    except Exception as e:
        print(f"Error sending onboarding email: {e}")
        return f"Error sending onboarding email: {str(e)}"