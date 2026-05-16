from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger("glowup.health")

@router.get("/")
def health_check():
    """
    Health check route to verify the API is running.
    """
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "message": "GlowUp API is healthy"}
