from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import logging
from app.services.chatbot import ProductRecommender

router = APIRouter()
logger = logging.getLogger("glowup.chatbot_route")
recommender = ProductRecommender()

class SkinContext(BaseModel):
    type: str
    concerns: List[str]

class ChatRequest(BaseModel):
    message: str
    skin_context: Optional[SkinContext] = None

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat_with_glowbot(request: ChatRequest):
    """
    Takes a user message and optional skin context to generate product recommendations.
    """
    logger.info(f"Received chat message: {request.message}")
    
    if request.skin_context:
        reply_text = recommender.recommend(
            skin_type=request.skin_context.type,
            concerns=request.skin_context.concerns
        )
    else:
        reply_text = "Hello! Please scan your skin first so I can give you personalized product recommendations!"
        
    return ChatResponse(reply=reply_text)
