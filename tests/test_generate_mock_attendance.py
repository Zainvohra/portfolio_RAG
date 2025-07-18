import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import timedelta, date, time
from app.database import SessionLocal
from app.models import Attendance, User

def random_time(start_hour=8, end_hour=10):
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    return time(hour, minute)

def random_leave():
    return random.choice([None, None, None, "sick", "vacation", "personal"])

def random_violations():
    return round(random.choice([0.0, 0.5, 1.0, 2.0, 4.0, 8.0]), 1)

def generate_dates(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)

def test_generate_mock_attendance():
    db = SessionLocal()
    user = db.query(User).first()
    if not user:
        user = User(name="Uzair Mustafa", email="uzair@folio3.com")
        db.add(user)
        db.commit()
        db.refresh(user)

    for d in generate_dates(date(2025, 5, 1), date(2025, 6, 30)):
        leave = random_leave()
        if leave:
            time_in = None
            time_out = None
            violations = 0.0
        else:
            time_in = random_time(8, 10)
            time_out = random_time(16, 18)
            violations = random_violations() if random.random() < 0.3 else 0.0

        attendance = Attendance(
            user_id=user.id,
            date=d,
            time_in=time_in,
            time_out=time_out,
            leave=leave,
            violations=violations
        )
        db.add(attendance)
    db.commit()
    db.close()
    print("Mock attendance data generated for May and June 2025.")

if __name__ == "__main__":
    test_generate_mock_attendance() 