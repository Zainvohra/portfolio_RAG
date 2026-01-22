"""
Dummy Data Generation Script
This script creates dummy users, line managers, and attendance records for testing purposes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import random
from datetime import timedelta, date, time
from app.database import SessionLocal
from app.models import Attendance, User, LineManager


def random_time(start_hour=8, end_hour=10):
    """Generate a random time within the specified hour range."""
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    return time(hour, minute)


def random_leave():
    """Generate a random leave type or None (most of the time None)."""
    return random.choice([None, None, None, None, None, "sick", "vacation", "personal"])


def calculate_work_hour_violations(time_in, time_out):
    """
    Calculate violations based on work hours.
    Expected work hours: 9 hours per day
    Violation: 1 point per hour short of 9 hours
    Decimal violations for partial hours (e.g., 0.5 for 30 minutes short)
    """
    if time_in is None or time_out is None:
        return 0.0
    
    # Convert time objects to total minutes
    time_in_minutes = time_in.hour * 60 + time_in.minute
    time_out_minutes = time_out.hour * 60 + time_out.minute
    
    # Handle case where time_out is next day (shouldn't happen in normal cases)
    if time_out_minutes < time_in_minutes:
        time_out_minutes += 24 * 60  # Add 24 hours in minutes
    
    # Calculate work duration in hours
    work_minutes = time_out_minutes - time_in_minutes
    work_hours = work_minutes / 60.0
    
    # Expected work hours is 9
    expected_hours = 9.0
    
    if work_hours < expected_hours:
        # Calculate violation: 1 point per hour short
        hours_short = expected_hours - work_hours
        return round(hours_short, 1)
    
    return 0.0


def random_additional_violations():
    """Generate random additional violation scores (for other types of violations)."""
    # 20% chance of having additional violations
    if random.random() < 0.2:
        return round(random.choice([0.5, 1.0, 2.0]), 1)
    return 0.0


def generate_realistic_work_times():
    """
    Generate realistic work times that may result in violations.
    Returns tuple of (time_in, time_out)
    """
    scenarios = [
        # Normal full day (9+ hours)
        {"weight": 60, "time_in_range": (8, 9), "work_hours_range": (9.0, 10.0)},
        # Slightly short day (8-8.9 hours) 
        {"weight": 20, "time_in_range": (8, 10), "work_hours_range": (8.0, 8.9)},
        # Short day (6-7.9 hours)
        {"weight": 15, "time_in_range": (9, 11), "work_hours_range": (6.0, 7.9)},
        # Very short day (4-5.9 hours)
        {"weight": 5, "time_in_range": (10, 12), "work_hours_range": (4.0, 5.9)},
    ]
    
    # Choose scenario based on weights
    total_weight = sum(s["weight"] for s in scenarios)
    rand = random.randint(1, total_weight)
    cumulative = 0
    
    for scenario in scenarios:
        cumulative += scenario["weight"]
        if rand <= cumulative:
            # Generate time_in
            time_in_hour = random.randint(*scenario["time_in_range"])
            time_in_minute = random.randint(0, 59)
            time_in = time(time_in_hour, time_in_minute)
            
            # Generate work duration
            work_hours = random.uniform(*scenario["work_hours_range"])
            
            # Calculate time_out
            time_in_minutes = time_in_hour * 60 + time_in_minute
            time_out_minutes = time_in_minutes + int(work_hours * 60)
            
            time_out_hour = (time_out_minutes // 60) % 24
            time_out_minute = time_out_minutes % 60
            time_out = time(time_out_hour, time_out_minute)
            
            return time_in, time_out
    
    # Fallback (shouldn't reach here)
    return random_time(8, 10), random_time(17, 19)


def generate_dates(start_date, end_date):
    """Generate all dates between start_date and end_date (inclusive)."""
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def create_users(db):
    """Create the 4 new users if they don't exist."""
    users_data = [
        {"name": "Zain", "email": "zain@folio3.com"},
        {"name": "Moatasim", "email": "moatasim@folio3.com"},
        {"name": "Shahzaib", "email": "shahzaib@folio3.com"},
        {"name": "Hunzala", "email": "hunzala@folio3.com"}
    ]
    
    created_users = []
    
    for user_data in users_data:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing_user:
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                onboarding_status=random.choice(["pending", "completed", "in_progress"])
            )
            db.add(user)
            created_users.append(user)
            print(f"Created user: {user_data['name']} ({user_data['email']})")
        else:
            created_users.append(existing_user)
            print(f"User already exists: {user_data['name']} ({user_data['email']})")
    
    db.commit()
    
    # Refresh all users to get their IDs
    for user in created_users:
        db.refresh(user)
    
    return created_users


def create_line_managers(db, users):
    """Create 4 random line managers from the users."""
    # Get all existing users to potentially assign as line managers
    all_users = db.query(User).all()
    
    if len(all_users) < 4:
        print("Warning: Not enough users to create 4 line managers")
        return []
    
    # Randomly select 4 users to be line managers
    selected_managers = random.sample(all_users, min(4, len(all_users)))
    
    created_managers = []
    
    for user in selected_managers:
        # Check if this user is already a line manager
        existing_manager = db.query(LineManager).filter(LineManager.user_id == user.id).first()
        if not existing_manager:
            line_manager = LineManager(user_id=user.id)
            db.add(line_manager)
            created_managers.append(line_manager)
            print(f"Created line manager for user: {user.name} (ID: {user.id})")
        else:
            created_managers.append(existing_manager)
            print(f"Line manager already exists for user: {user.name} (ID: {user.id})")
    
    db.commit()
    
    # Refresh all line managers to get their IDs
    for manager in created_managers:
        db.refresh(manager)
    
    return created_managers


def create_attendance_records(db, users, start_date, end_date):
    """Create attendance records for all users for the specified date range."""
    total_records = 0
    total_violations = 0

    for user in users:
        print(f"Generating attendance records for {user.name}...")
        user_violations = 0

        for d in generate_dates(start_date, end_date):
            # Check if attendance record already exists for this user and date
            existing_record = db.query(Attendance).filter(
                Attendance.user_id == user.id,
                Attendance.date == d
            ).first()

            if existing_record:
                continue  # Skip if record already exists

            leave = random_leave()
            if leave:
                # If on leave, no time_in/time_out and no violations
                time_in = None
                time_out = None
                violations = 0.0
            else:
                # Normal working day - generate realistic work times
                time_in, time_out = generate_realistic_work_times()

                # Calculate work hour violations
                work_hour_violations = calculate_work_hour_violations(time_in, time_out)

                # Add any additional random violations
                additional_violations = random_additional_violations()

                # Total violations
                violations = round(work_hour_violations + additional_violations, 1)

                if violations > 0:
                    user_violations += violations

            attendance = Attendance(
                user_id=user.id,
                date=d,
                time_in=time_in,
                time_out=time_out,
                leave=leave,
                violations=violations
            )
            db.add(attendance)
            total_records += 1

        if user_violations > 0:
            print(f"  - {user.name} total violations: {user_violations}")
        total_violations += user_violations

    db.commit()
    print(f"Created {total_records} attendance records")
    print(f"Total violations across all users: {total_violations}")


def generate_dummy_data():
    """Main function to generate all dummy data."""
    print("Starting dummy data generation...")

    db = SessionLocal()

    try:
        # Create users
        print("\n1. Creating users...")
        users = create_users(db)

        # Create line managers
        print("\n2. Creating line managers...")
        line_managers = create_line_managers(db, users)

        # Create attendance records for 2 months (current example: May and June 2025)
        print("\n3. Creating attendance records...")
        start_date = date(2025, 1, 1)
        end_date = date(2025, 7, 31)
        create_attendance_records(db, users, start_date, end_date)

        print(f"\n✅ Dummy data generation completed successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(line_managers)} line managers")
        print(f"Generated attendance records from {start_date} to {end_date}")

    except Exception as e:
        print(f"❌ Error during dummy data generation: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_dummy_data()
