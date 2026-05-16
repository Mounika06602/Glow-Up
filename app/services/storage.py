import os
import uuid
from PIL import Image
from app.core.config import settings

def save_image_locally(image: Image.Image, original_filename: str) -> str:
    """
    Saves a Pillow image locally based on UPLOAD_DIR.
    Returns the file path.
    """
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
        
    # Generate a unique filename to prevent collisions
    ext = original_filename.split(".")[-1] if "." in original_filename else "jpg"
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save the image
    image.save(file_path)
    
    return file_path
