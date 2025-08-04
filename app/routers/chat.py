import structlog
from fastapi import Response

from app.services.agents import query_pulse_ai_mcp, query_pulse_ai
from app.services.emails import send_email
from fastapi import APIRouter
from app.schemas import PulseAIPayload


router = APIRouter(prefix="/pulse/chat")


@router.get("/health")
async def health_check():
    """Health check endpoint to test API connectivity"""
    try:
        from app.services.agents import GEMINI_API_KEY
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
    return {"message": "OK"}

@router.post("/")
@router.post("")  # Handle both /pulse/chat/ and /pulse/chat
async def chat(payload: PulseAIPayload):
    logger = structlog.get_logger()

    try:
        logger.info("Received chat request", query=payload.query)
        # for running the agent with function tools or rag
        # inference = await query_pulse_ai(payload.query)
        # for running the agent with mcp tools
        inference = await query_pulse_ai_mcp(payload.query)

        logger.info("Chat response generated", response=inference)

        return inference
    except Exception as e:
        logger.error("Error in chat endpoint", error=str(e))
        return Response(
            content=f"Error processing request: {str(e)}", 
            media_type="application/json",
            status_code=500
        )
