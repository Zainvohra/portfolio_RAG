import structlog
from fastapi import Response
from fastapi.responses import JSONResponse

from app.services.agent_init import query_pulse_ai_mcp, query_pulse_ai
from app.services.emails import send_email
from fastapi import APIRouter
from app.schemas import PulseAIPayload


router = APIRouter(prefix="/pulse/chat")


@router.get("/health")
async def health_check():
    """Health check endpoint to test API connectivity"""
    try:
        from app.services.agent_init import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            return Response(
                content="Error: GEMINI_API_KEY not configured", 
                media_type="application/json",
                status_code=500
            )
        return Response(
            content="MCP + Gemini API configured", 
            media_type="application/json",
            status_code=200
        )
    except Exception as e:
        return Response(
            content=f"Health check failed: {str(e)}", 
            media_type="application/json",
            status_code=500
        )


@router.options("/")
@router.options("")  # Handle CORS preflight for both paths
async def chat_options():
    return Response(
        content="OK",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )

@router.post("/")
@router.post("")  # Handle both /pulse/chat/ and /pulse/chat
async def chat(payload: PulseAIPayload):
    logger = structlog.get_logger()

    try:
        logger.info("Received chat request", query=payload.query)
        # for running the agent with function tools or rag
        inference = await query_pulse_ai(payload.query)
        # for running the agent with mcp tools
        # inference = await query_pulse_ai_mcp(payload.query)

        logger.info("Chat response generated", response=inference)

        # Return as JSON response with explicit CORS headers
        return JSONResponse(
            content={"response": inference},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
        )
    except Exception as e:
        logger.error("Error in chat endpoint", error=str(e))
        return Response(
            content=f"Error processing request: {str(e)}", 
            media_type="application/json",
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
            }
        )
