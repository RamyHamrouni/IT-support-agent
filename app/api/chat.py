from fastapi import APIRouter, Request
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):
    categories = request.app.state.all_categories
    return await process_chat(req, categories)