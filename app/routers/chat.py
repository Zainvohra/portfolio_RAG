import structlog
from fastapi import Response

from app.services.agents import query_pulse_ai
from app.services.emails import send_email
from fastapi import APIRouter
from app.schemas import PulseAIPayload


router = APIRouter(prefix="/pulse/chat")


@router.get("/health")
async def health_check():
    """Health check endpoint to test API connectivity"""
    try:
        from app.services.agents import GROQ_API_KEY, GROQ_BASE_URL
        if not GROQ_API_KEY:
            return Response(
                content="Error: GROQ_API_KEY not configured", 
                media_type="application/json",
                status_code=500
            )
        return Response(
            content="API key configured", 
            media_type="application/json",
            status_code=200
        )
    except Exception as e:
        return Response(
            content=f"Health check failed: {str(e)}", 
            media_type="application/json",
            status_code=500
        )


@router.post("/")
async def chat(payload: PulseAIPayload):
    logger = structlog.get_logger()

    try:
        logger.info("Received chat request", query=payload.query)

        inference = await query_pulse_ai(payload.query)

        logger.info("Chat response generated", response=inference)

        return inference
    except Exception as e:
        logger.error("Error in chat endpoint", error=str(e))
        return Response(
            content=f"Error processing request: {str(e)}", 
            media_type="application/json",
            status_code=500
        )
