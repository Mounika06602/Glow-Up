from fastapi import APIRouter
from app.api.routes import health, scan, chatbot

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(scan.router, prefix="/scan", tags=["scan"])
api_router.include_router(chatbot.router, prefix="/chat", tags=["chat"])
