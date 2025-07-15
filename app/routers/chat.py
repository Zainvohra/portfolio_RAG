import structlog
from fastapi import Response

from app.services.agents import query_pulse_ai
from app.services.emails import send_email
from fastapi import APIRouter
from app.schemas import PulseAIPayload


router = APIRouter(prefix="/pulse/chat")


@router.post("/")
async def chat(payload: PulseAIPayload):
    logger = structlog.get_logger()

    logger.info("Received chat request", query=payload.query)

    inference = await query_pulse_ai(payload.query)

    await send_email(
        to="abc@xyz.com",
        subject="Your Pulse AI Response",
        body=f"Here is your response: {inference}",
    )

    logger.info("Chat response generated", response=inference)

    return Response(content=inference, media_type="application/json")
