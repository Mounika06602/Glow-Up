from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.main_router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
import logging
import os

# Set up centralized logging
logger = setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for GlowUp - Beauty products review for all skin types.",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Ensure upload directory exists and mount it for static file serving
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}...")

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API. Visit /docs for API documentation."}
