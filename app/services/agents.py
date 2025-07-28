from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
import os
from dotenv import load_dotenv
from datetime import date
import json
from agents.extensions.models.litellm_model import LitellmModel
from app.services.attendance import AttendanceService
from app.schemas import GetAttendanceReportRequest
from app.database import SessionLocal
from app.services.onboarding_email import OnboardingEmailService
from rag.rag_tools import rag_search_tool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)

if not OPENAI_API_KEY or not GEMINI_API_KEY:
    raise ValueError("LLM API Keys are required")

PULSE_AI_INSTRUCTIONS = """
You are PulseAI, a concise assistant that can call any registered tool.

1. Handle small talk and pleasantries with a brief friendly reply—do not invoke any tools.
2. Determine which tool fits the user’s request and extract/normalize its parameters (e.g., “May 3–5” → 2025-05-03 to 2025-05-05).
3. If any parameter is missing or ambiguous, ask one concise follow-up question.
4. Invoke the tool; it will return one of:
   • Plain text → echo it verbatim.  
   • JSON → parse it:  
     – Summarize the high-level result in 1–2 sentences.  
     – Highlight any key issues or flags.  
     – If “detail” or “daily breakdown” is requested, include a brief itemized section.  
   • An error → respond in one sentence: “Sorry, I couldn’t fetch [X] because [reason].”
5. If no tool applies, reply: “I’m not sure how to help with that—could you rephrase?”
6. Keep all replies under 3 bullet points or one short paragraph, in natural language.
7. Every response should be of atleast two lines.
"""

PULSE_RAG_AI_INSTRUCTIONS = """You are an intelligent RAG (Retrieval Augmented Generation) assistant specialized in answering questions about the employee handbook.
Your primary function is to help users find information from the company's employee handbook. When users ask questions, you should:

1. Use the rag_search_tool to search the employee handbook content
2. Always use the index name 'employee_handbook' when calling the search tool
3. Provide clear, helpful answers based on the retrieved information
4. If the information isn't found in the handbook, clearly state that
5. Focus only on employee handbook related queries

You have access to semantic search capabilities that can find relevant information even when the exact words don't match the query.
"""


def _get_attendance_report_logic(user_id: int, start_date: str, end_date: str) -> str:
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


@function_tool
def get_attendance_report(user_id: int, start_date: str, end_date: str) -> str:
    """Get attendance report for a user within a date range."""
    return _get_attendance_report_logic(user_id, start_date, end_date)


@function_tool
def get_missing_attendance_user_ids(start_date: str, end_date: str) -> str:
    """Returns a list of user IDs with missing attendance records, violations or leaves."""
    return _get_missing_attendance_user_ids(start_date, end_date)


def _get_missing_attendance(user_id: int, start_date: str, end_date: str) -> str:
    """Get missing attendance records for a user within a date range."""
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
    except Exception as e:
        print(f"Error in _get_attendance_report_logic: {str(e)}")
        return f"Error generating attendance report: {str(e)}"


@function_tool
def get_missing_attendance(user_id: int, start_date: str, end_date: str) -> str:
    """Get missing attendance records for a user within a date range."""
    response = _get_missing_attendance(user_id, start_date, end_date)
    return response


async def _send_onboarding_email(user_id: int) -> str:
    """Send onboarding email to the user with the given user_id if their onboarding status is pending."""
    db = SessionLocal()
    try:
        service = OnboardingEmailService(db)
        result = await service.send_onboarding_email_to_user(user_id)
        return result
    finally:
        db.close()


@function_tool
async def send_onboarding_email(user_id: int) -> str:
    """Send onboarding email to the user with the given user_id if not already sent."""
    response = await _send_onboarding_email(user_id=user_id)
    return response


def get_agent():
    agent = Agent(
        name="PulseAI",
        instructions=PULSE_AI_INSTRUCTIONS,
        model=OpenAIChatCompletionsModel(
            model="gpt-4o", openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY)
        ),
        tools=[
            get_attendance_report,
            get_missing_attendance,
            send_onboarding_email,
            get_missing_attendance_user_ids,
        ],
    )
    return agent

def get_rag_agent():
    agent = Agent(
            name="Employee Handbook RAG Assistant",
            instructions=PULSE_RAG_AI_INSTRUCTIONS,
            model=LitellmModel(
            model="gemini/gemini-2.0-flash-exp",
            api_key=GEMINI_API_KEY,
            ),
            tools=[
                rag_search_tool
            ]
        )
    return agent

async def query_pulse_ai(query: str):
    try:
        # For Tool Calling Agent
        # agent = get_agent()
        # For RAG Agent
        agent = get_rag_agent()
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
