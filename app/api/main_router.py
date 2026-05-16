from fastapi import APIRouter
from app.api.routes import health, scan

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(scan.router, prefix="/scan", tags=["scan"])
