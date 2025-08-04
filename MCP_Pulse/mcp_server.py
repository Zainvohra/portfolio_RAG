

import asyncio
import json
from datetime import date
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from app.helpers.utils import (
    _get_attendance_report_logic,
    _get_missing_attendance_user_ids,
    _get_missing_attendance,
    _send_onboarding_email
)

load_dotenv()

# Create FastMCP server
mcp = FastMCP("PulseAI MCP Tools Server")

# MCP Tools
@mcp.tool()
def get_attendance_report(user_id: int, start_date: str, end_date: str) -> str:
    """Get attendance report for a user within a date range."""
    print(f"🔧 [MCP-TOOL-CALLED] get_attendance_report({user_id}, {start_date}, {end_date})")
    result = _get_attendance_report_logic(user_id, start_date, end_date)
    print(f"🔧 [MCP-TOOL-RESULT] get_attendance_report → {result[:100]}...")
    return result

@mcp.tool()
def get_missing_attendance_user_ids(start_date: str, end_date: str) -> str:
    """Returns a list of user IDs with missing attendance records, violations or leaves."""
    print(f"🔧 [MCP-TOOL-CALLED] get_missing_attendance_user_ids({start_date}, {end_date})")
    result = _get_missing_attendance_user_ids(start_date, end_date)
    print(f"🔧 [MCP-TOOL-RESULT] get_missing_attendance_user_ids → {result[:100]}...")
    return result

@mcp.tool()
def get_missing_attendance(user_id: int, start_date: str, end_date: str) -> str:
    """Get missing attendance records for a user within a date range."""
    print(f"🔧 [MCP-TOOL-CALLED] get_missing_attendance({user_id}, {start_date}, {end_date})")
    result = _get_missing_attendance(user_id, start_date, end_date)
    print(f"🔧 [MCP-TOOL-RESULT] get_missing_attendance → {result[:100]}...")
    return result

@mcp.tool()
async def send_onboarding_email(user_id: int) -> str:
    """Send onboarding email to the user with the given user_id if not already sent."""
    print(f"🔧 [MCP-TOOL-CALLED] send_onboarding_email({user_id})")
    result = await _send_onboarding_email(user_id=user_id)
    print(f"🔧 [MCP-TOOL-RESULT] send_onboarding_email → {result[:100]}...")
    return result

# Simple test tools like in the reference
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"🔧 [MCP-TOOL-CALLED] add({a}, {b})")
    result = a + b
    print(f"🔧 [MCP-TOOL-RESULT] add → {result}")
    return result

@mcp.tool()
def get_pulse_status() -> str:
    """Get the current status of PulseAI system"""
    print(f"🔧 [MCP-TOOL-CALLED] get_pulse_status()")
    result = "PulseAI system is running and ready to assist with attendance, onboarding, and other HR tasks."
    print(f"🔧 [MCP-TOOL-RESULT] get_pulse_status → {result}")
    return result

if __name__ == "__main__":
    print("🚀 Starting PulseAI MCP Server...")
    print("📍 Server URL: http://localhost:8000/sse")
    print("🔧 Registered Tools:")
    print("  ✅ add(a, b) - Add two numbers")
    print("  ✅ get_pulse_status() - Get system status")  
    print("  ⚠️  get_attendance_report() - Needs database")
    print("  ⚠️  get_missing_attendance() - Needs database")
    print("  ⚠️  get_missing_attendance_user_ids() - Needs database")
    print("  ⚠️  send_onboarding_email() - Needs database")
    print("=" * 60)
    print("🎯 Watch for [MCP-TOOL-CALLED] and [MCP-TOOL-RESULT] messages")
    print("=" * 60)
    mcp.run(transport="sse") 