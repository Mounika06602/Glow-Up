from fastapi import APIRouter, File, UploadFile, HTTPException
import logging
import os
from app.services.image_validator import validate_image
from app.services.storage import save_image_locally
from app.services.pipeline import SkinAnalysisPipeline
from app.schemas.analysis import SkinAnalysisResponse

router = APIRouter()
logger = logging.getLogger("glowup.scan")
pipeline = SkinAnalysisPipeline()

@router.post("/", response_model=SkinAnalysisResponse)
async def scan_product(file: UploadFile = File(...)):
    """
    Scans a beauty product image to extract information.
    Validates that the file is an image, saves it locally, and runs the AI pipeline.
    """
    logger.info(f"Received scan request for file: {file.filename}")
    
    try:
        # Validate the image using our service
        image = validate_image(file)
        logger.info(f"Image validated successfully. Format: {image.format}, Size: {image.size}")
        
        # Save the image locally
        file_path = save_image_locally(image, file.filename)
        logger.info(f"Image saved locally at {file_path}")
        
        # Pass the image path to our Skin Analysis Pipeline
        analysis_result = pipeline.analyze(file_path)
        
        # Construct a response with a dummy image URL for now
        # In the future, this might be a static mount or an S3 URL
        image_url = f"/uploads/{os.path.basename(file_path)}"
        
        return SkinAnalysisResponse(
            status="success",
            message="Image scanned successfully",
            image_url=image_url,
            analysis=analysis_result
        )
    except HTTPException as e:
        logger.error(f"Validation failed for {file.filename}: {e.detail}")
        raise e
    except Exception as e:
        import traceback
        logger.error(f"Unexpected error during scan: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
