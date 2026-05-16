from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
import json

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Dermatology Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # MongoDB
    MONGODB_URL: Optional[str] = None
    MONGODB_DB: Optional[str] = None
    
    # Redis
    REDIS_URL: Optional[str] = None
    
    # PostgreSQL
    POSTGRES_URL: Optional[str] = None
    
    # Supabase
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    # Cloudinary
    CLOUDINARY_URL: Optional[str] = None
    
    # AWS S3
    S3_BUCKET: Optional[str] = None
    S3_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # Auth / JWT
    SECRET_KEY: str = "change-me-in-production-use-secrets-token-hex-32"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = ["*"]
    
    # Storage paths
    MODEL_DIR: str = "models/"
    UPLOAD_DIR: str = "backend/storage/uploads"
    
    # ML Models
    YOLO_MODEL_PATH: str = "yolov8n.pt" # Default to base YOLOv8 model if none provided

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def get_cors_origins(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            try:
                return json.loads(self.CORS_ORIGINS)
            except Exception:
                return [i.strip() for i in self.CORS_ORIGINS.split(",") if i.strip()]
        return self.CORS_ORIGINS

settings = Settings()
