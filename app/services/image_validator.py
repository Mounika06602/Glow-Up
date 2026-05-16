from fastapi import UploadFile, HTTPException
from PIL import Image
import io

def validate_image(file: UploadFile) -> Image.Image:
    """
    Validates that the uploaded file is a valid image.
    Returns a PIL Image object if valid, raises an HTTPException otherwise.
    """
    # Check content type first
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail=f"File '{file.filename}' is not an image.")

    try:
        # Read the file content
        content = file.file.read()
        
        # Reset the file pointer so it can be read again if needed
        file.file.seek(0)
        
        # Try to open the image with Pillow
        image = Image.open(io.BytesIO(content))
        
        # Verify the image (catches truncated/corrupt files)
        image.verify()
        
        # Re-open the image because verify() closes it or leaves it in an unusable state
        image = Image.open(io.BytesIO(content))
        
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
