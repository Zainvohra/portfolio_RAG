from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
import os
from dotenv import load_dotenv
from datetime import date
import json

from app.services.attendance import AttendanceService
from app.schemas import GetAttendanceReportRequest
from app.database import SessionLocal

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", None)
MODEL = "llama-3.3-70b-versatile"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

PULSE_AI_INSTRUCTIONS = """
You are a helpful assistant that can provide attendance reports.

CRITICAL INSTRUCTIONS:
1. When users ask for attendance information, you MUST use the get_attendance_report tool.
2. Extract user_id from the query (e.g., "user 1" means user_id=1, "user 5" means user_id=5).
3. Parse date ranges from the query and convert them to YYYY-MM-DD format.
4. If no year is mentioned in date requests, use the current year, otherwise use the year mentioned in the date range.
5. Call the get_attendance_report tool with the extracted user_id, start_date, and end_date.
6. The tool will return JSON data with attendance records.
7. Parse the JSON data and calculate statistics (work days, leave days, average hours, etc.).
8. ALWAYS check for violations in the data and highlight them prominently.
9. Provide a natural, conversational response with clear sections.
10. Use natural language to explain the attendance patterns.
11. For follow-up questions about "daily breakdown", "day by day", or "each day", use the same user_id and date range from the previous query.

TOOL SELECTION GUIDELINES:
- Use get_attendance_report for: "attendance report", "attendance data", "attendance records", "attendance summary"
- Use get_missing_attendance for: "missing attendance", "absent days", "no show", "didn't come to work", "missed work"
- If the query mentions "missing" or "absent" specifically, wait for the get_missing_attendance tool to be available.

RESPONSE FORMAT:
"Here's your attendance report for [date range]:

📊 **Summary:**
[Calculate and explain attendance rate, average hours, etc.]

⚠️ **Violations & Issues:**
• [List any violations, missing clock-ins/outs, etc.]

🏥 **Key Insights:**
• [List important patterns and insights]

📅 **Daily Breakdown:**
• [Only include daily breakdown if user explicitly asks for it]"

IMPORTANT: 
- You MUST call the get_attendance_report tool with proper parameters before providing any response.
- Extract user_id as a number from phrases like "user 1", "user 5", etc.
- Convert date ranges to YYYY-MM-DD format (e.g., "May 10 to 15" becomes "2025-05-10" to "2025-05-15").
- Use 2025 as the default year since that's where the test data exists.
- After calling the tool, you MUST process the JSON data and provide the formatted response.
- Do NOT return the raw tool call.
- ALWAYS check the 'violations' field in each record and 'total_violations' in the response.
- Highlight violations prominently in the response.
- If the tool returns an error, explain the error to the user.
- For queries about "missing attendance", inform the user that a specialized tool will be available soon.
- Only include daily breakdown section if user explicitly asks for "daily breakdown", "day by day", "each day", or similar phrases.
- For follow-up questions without new user_id or date range, use the context from the previous query.
"""

async def _get_attendance_report_logic(user_id: int, start_date: str, end_date: str) -> str:
    try:
        print(f"Getting attendance report for user {user_id} from {start_date} to {end_date}")
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        db = SessionLocal()
        try:
            attendance_service = AttendanceService(db)
            request = GetAttendanceReportRequest(
                user_id=user_id,
                start_date=start,
                end_date=end
            )
            report = attendance_service.get_attendance_report(request)
            result = json.dumps({
                "user_id": report.user_id,
                "start_date": report.start_date.isoformat(),
                "end_date": report.end_date.isoformat(),
                "total_violations": report.total_violations,
                "records": [
                    {
                        "date": record.date.isoformat(),
                        "time_in": record.time_in.isoformat() if record.time_in else None,
                        "time_out": record.time_out.isoformat() if record.time_out else None,
                        "leave": record.leave,
                        "violations": record.violations
                    }
                    for record in report.records
                ]
            })
            print(f"Successfully generated report with {len(report.records)} records")
            return result
        finally:
            db.close()
    except Exception as e:
        print(f"Error in _get_attendance_report_logic: {str(e)}")
        return f"Error generating attendance report: {str(e)}"

@function_tool
async def get_attendance_report(user_id: int, start_date: str, end_date: str) -> str:
    """Get attendance report for a user within a date range."""
    return await _get_attendance_report_logic(user_id, start_date, end_date)

async def query_pulse_ai(query: str):
    try:
        groq_model = OpenAIChatCompletionsModel(
            model=MODEL,
            openai_client=AsyncOpenAI(
                base_url=GROQ_BASE_URL,
                api_key=GROQ_API_KEY,
                timeout=30.0,
                max_retries=3,
            ),
        )

        agent = Agent(
            name="PulseAI",
            instructions=PULSE_AI_INSTRUCTIONS,
            model=groq_model,
            tools=[get_attendance_report]
        )

        result = await Runner.run(agent, input=query)
        return result.final_output
    except Exception as e:
        print(f"Error in query_pulse_ai: {str(e)}")
        print(f"Error type: {type(e)}")
        if "write could not complete without blocking" in str(e):
            return "Error: Connection timeout with the AI service. Please try again in a moment."
        elif "timeout" in str(e).lower():
            return "Error: Request timed out. Please try again."
        elif "GROQ_API_KEY" in str(e):
            return "Error: AI service configuration issue. Please check API key."
        else:
            return f"Error processing your request: {str(e)}"
