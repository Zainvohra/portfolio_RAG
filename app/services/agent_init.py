from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, SQLiteSession
import os
from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel
from agents.model_settings import ModelSettings
from rag.rag_tools import rag_portfolio_tool
from app.helpers.utils import _get_attendance_report_logic, _get_missing_attendance_user_ids, _get_missing_attendance, _send_onboarding_email
# MCP imports
from agents.mcp import MCPServer, MCPServerSse
from typing import List

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)


''' ------------------------------------------------------------------------------------------------------------------------------
 Below is the production level Pipedream SDK managed implementation of an GMail MCP server with production-grade OAuth management,
 specifically for the case where we have multiple users each logging in with their own GMail account. 

# from pipedream import Pipedream
# from openai import OpenAI

pd = Pipedream(
    project_id=os.getenv('PIPEDREAM_PROJECT_ID', None),
    project_environment=os.getenv('PIPEDREAM_ENVIRONMENT', None),
    client_id=os.getenv('PIPEDREAM_CLIENT_ID', None),
    client_secret=os.getenv('PIPEDREAM_CLIENT_SECRET', None)
)
app_slug = "gmail"
# Get access token for MCP server auth
access_token = await pd.raw_access_token

# Send the unique ID that you use to identify this user in your system
external_user_id = 'abc-123'  # Used in MCP URL to identify the user

# Initialize OpenAI client
client = openai.OpenAI()

# Make the OpenAI request with the MCP server
response = client.responses.create(
    model='gpt-4.1',
    tools=[
        {
            "type": "mcp",
            "server_label": app_slug,
            "server_url": "https://remote.mcp.pipedream.net",
            "headers": {
                "Authorization": f"Bearer {access_token}",
                "x-pd-project-id": PIPEDREAM_PROJECT_ID,
                "x-pd-environment": PIPEDREAM_ENVIRONMENT,
                "x-pd-external-user-id": external_user_id,
                "x-pd-app-slug": app_slug,
            },
            "require_approval": "never"
        }
    ],
    input='Summarize my latest email in my inbox.'
)

print(response)

---------------------------------------------------------------------------------------------------------------------------------------
'''

PULSE_AI_INSTRUCTIONS = """
You are PulseAI, a concise assistant that can call any registered tool.

1. Handle small talk and pleasantries with a brief friendly reply—do not invoke any tools.
2. Determine which tool fits the user's request and extract/normalize its parameters (e.g., "May 3–5" → 2025-05-03 to 2025-05-05).
3. If any parameter is missing or ambiguous, ask one concise follow-up question.
4. Invoke the tool; it will return one of:
   • Plain text → echo it verbatim.  
   • JSON → parse it:  
     – Summarize the high-level result in 1–2 sentences.  
     – Highlight any key issues or flags.  
     – If "detail" or "daily breakdown" is requested, include a brief itemized section.  
   • An error → respond in one sentence: "Sorry, I couldn't fetch [X] because [reason]."
5. If no tool applies, reply: "I'm not sure how to help with that—could you rephrase?"
6. Keep all replies under 3 bullet points or one short paragraph, in natural language.
7. Every response should be of atleast two lines.
"""

PULSE_RAG_AI_INSTRUCTIONS = """You are an intelligent RAG (Retrieval Augmented Generation) assistant specialized in answering questions about Zainul Abideen Vohra's portfolio, professional experience, and achievements.

Your primary function is to help users learn about Zain ul Abideen Vohra (referred to as "Zain" or "he/him") by providing detailed information from his portfolio data.

IMPORTANT: Always refer to Zain ul Abideen Vohra in the third person. Use "he", "his", "him", "Zain", - NEVER use "you", "your", or "I" when referring to him.

When users ask questions, you should:

1. For portfolio-related questions (projects, experience, skills, technologies, achievements, education):
   - Use the rag_portfolio_tool to search in portfolio data
   - This includes questions about: projects Zain has worked on, technologies he has used, his work experience, achievements, skills, education, certifications, etc.
   - Provide detailed, engaging answers that highlight relevant projects and experiences
   - When discussing projects, include key technologies, challenges solved, and impact
   - Always frame responses in third person (e.g., "Zain worked on...", "He has experience with...", "His projects include...")

2. General guidelines:
   - Always use third person when referring to Zain ul Abideen Vohra
   - If the information isn't found, clearly state that the information is not available in the portfolio
   - Provide basic, engaging answers that showcase Zain's expertise and achievements
   - When discussing technical skills, be specific about technologies, frameworks, and tools
   - Highlight notable achievements, impact, and contributions
   - Be professional and accurate in all responses
   - If asked about Zain directly (e.g., "Tell me about Zain", "What does Zain do?"), provide a comprehensive overview of his background, skills, and experience

You have access to semantic search capabilities that can find relevant information even when the exact words don't match the query.
"""

session = SQLiteSession("user_random")

# Keep original function_tool versions for backward compatibility
@function_tool
def get_attendance_report_ft(user_id: int, start_date: str, end_date: str) -> str:
    """Get attendance report for a user within a date range."""
    return _get_attendance_report_logic(user_id, start_date, end_date)

@function_tool
def get_missing_attendance_user_ids_ft(start_date: str, end_date: str) -> str:
    """Returns a list of user IDs with missing attendance records, violations or leaves."""
    return _get_missing_attendance_user_ids(start_date, end_date)

@function_tool
def get_missing_attendance_ft(user_id: int, start_date: str, end_date: str) -> str:
    """Get missing attendance records for a user within a date range."""
    response = _get_missing_attendance(user_id, start_date, end_date)
    return response

@function_tool
async def send_onboarding_email_ft(user_id: int) -> str:
    """Send onboarding email to the user with the given user_id if not already sent."""
    response = await _send_onboarding_email(user_id=user_id)
    return response

# async def run_with_mcp_server(mcp_servers: List[MCPServer], query: str) -> str:
#     """Run a query using the MCP server (following reference pattern)"""
#     agent = Agent(
#         name="PulseAI Assistant",
#         instructions=PULSE_AI_INSTRUCTIONS,
#         mcp_servers=[mcp_servers],
#         model_settings=ModelSettings(tool_choice="auto"),
#         model=LitellmModel(
#             model="gemini/gemini-2.0-flash-exp",
#             api_key=GEMINI_API_KEY,
#         ),
#     )
#
#     print(f"Running: {query}")
#     result = await Runner.run(starting_agent=agent, input=query)
#     return result.final_output

def get_agent():
    """Original function tool based agent"""
    agent = Agent(
        name="PulseAI",
        instructions=PULSE_AI_INSTRUCTIONS,
        model=OpenAIChatCompletionsModel(
            model="gpt-4o", openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY)
        ),
        tools=[
            get_attendance_report_ft,
            get_missing_attendance_ft,
            send_onboarding_email_ft,
            get_missing_attendance_user_ids_ft,
        ],
    )
    return agent

def get_rag_agent():
    """RAG agent using Gemini model for portfolio queries"""
    agent = Agent(
            name="Zain ul Abideen Vohra Portfolio RAG Assistant",
            instructions=PULSE_RAG_AI_INSTRUCTIONS,
            model=LitellmModel(
            model="gemini/gemini-2.5-flash-lite",
            api_key=GEMINI_API_KEY,
    #          model="claude-3-5-sonnet-20241022",  # or another Claude model name
    # api_key=ANTHROPIC_API_KEY,
            ),
            tools=[
                rag_portfolio_tool
            ]
        )
    return agent


# Main query functions
async def query_pulse_ai(query: str):
    """Main query function - uses function tools for stability"""
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

async def query_pulse_ai_mcp(query: str):
    """Query using MCP-based agent with async context manager """
    try:
        async with MCPServerSse(
            name="PulseAI Tools Server",
            params={
                "url": "http://localhost:8000/sse",  # FastMCP default port
            },
        ) as pulse_local_server:
        # MCPServerSse(
        #     name="Pipedream Gmail Server",
        #     params={
        #         "url": os.getenv('GMAIL_MCP_URL'),
        #     },
        #     client_session_timeout_seconds=60,
        # ) as gmail_server:
            print(f"🤖 MCP Query: {query}")

            # Pass both into the function that creates the Agent
            # Instantiate the agent here, using both servers
            agent = Agent(
                name="PulseAI Assistant",
                instructions=PULSE_AI_INSTRUCTIONS,
                mcp_servers=[pulse_local_server],
                model_settings=ModelSettings(tool_choice="auto"),
                model=LitellmModel(
                    model="gemini/gemini-2.5-flash-lite",
                    api_key=GEMINI_API_KEY,
                ),
            )

            result = await Runner.run(starting_agent=agent, input=query, session=session)
            print(f"🎯 MCP Result: {result.final_output[:100]}...")
            return result.final_output
    except Exception as e:
        print(f"Error in query_pulse_ai_mcp: {str(e)}")
        print(f"Error type: {type(e)}")
        if "write could not complete without blocking" in str(e):
            return "Error: Connection timeout with the AI service. Please try again in a moment."
        elif "timeout" in str(e).lower():
            return "Error: Request timed out. Please try again."
        elif "Connection refused" in str(e) or "Connection error" in str(e):
            return "Error: MCP server not running. Please start the MCP server first."
        else:
            return f"Error processing your request: {str(e)}"
