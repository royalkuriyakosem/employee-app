"Ageent Router"

from fastapi import APIRouter
from agent.agent_config import chat
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/chat")
async def chat_router(body: dict[str, str]):
    return StreamingResponse(chat(body["prompt"]), media_type="text/event-stream")
