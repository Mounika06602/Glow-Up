import logging
import time
import os
import cv2
import random
import numpy as np
from PIL import Image, ImageDraw
from app.schemas.analysis import SkinAnalysisResult, AcneReport
from app.services.storage import save_image_locally
from app.ml.ml_models import FaceDetector, AcneDetector

logger = logging.getLogger("glowup.pipeline")

class SkinAnalysisPipeline:
    def __init__(self):
        logger.info("Initializing Skin Analysis Pipeline with ML models...")
        self.face_detector = FaceDetector()
        self.acne_detector = AcneDetector()
        
    def _generate_heatmap(self, image_path: str, detections: list, face_bbox: tuple = None) -> str:
        """
        Reads the original image, draws bounding boxes around detections, and saves it.
        Returns the filename/url of the heatmap.
        """
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                heatmap = img.copy()
                draw = ImageDraw.Draw(heatmap)
                
                width, height = img.size
                line_width = max(1, int(width * 0.005))
                
                # Optionally draw face bounding box (in blue)
                if face_bbox:
                    fx, fy, fw, fh = face_bbox
                    draw.rectangle([fx, fy, fx + fw, fy + fh], outline="blue", width=line_width)
                
                # Draw acne detections (in red)
                for det in detections:
                    x1, y1, x2, y2 = det['x1'], det['y1'], det['x2'], det['y2']
                    draw.rectangle([x1, y1, x2, y2], outline="red", width=line_width)
                    # Optional: draw confidence
                    # draw.text((x1, max(0, y1 - 10)), f"{det['confidence']:.2f}", fill="red")
                
                original_filename = os.path.basename(image_path)
                heatmap_filename = f"heatmap_{original_filename}"
                
                heatmap_path = save_image_locally(heatmap, heatmap_filename)
                
                return f"/uploads/{os.path.basename(heatmap_path)}"
        except Exception as e:
            logger.error(f"Failed to generate heatmap: {e}")
            return ""

    def analyze(self, image_path: str) -> SkinAnalysisResult:
        """
        Runs the full AI pipeline on the given image.
        """
        logger.info(f"Running ML pipeline on {image_path}")
        
        # Load image with OpenCV for ML models
        cv_image = cv2.imread(image_path)
        if cv_image is None:
            logger.error(f"Failed to load image at {image_path} with OpenCV.")
            raise ValueError("Invalid image file.")
            
        # 1. Face Detection
        face_bbox = self.face_detector.detect_face(cv_image)
        if face_bbox:
            logger.info(f"Face detected at {face_bbox}")
        else:
            logger.warning("No face detected, proceeding with full image analysis.")
            
        # 2. Acne Detection (YOLO)
        # We pass the full image. YOLO handles resizing.
        detections = self.acne_detector.detect(cv_image)
        
        # Optional: If face_bbox exists, filter detections that are outside the face
        if face_bbox:
            fx, fy, fw, fh = face_bbox
            filtered_detections = []
            for det in detections:
                # Center of the detection
                cx = (det['x1'] + det['x2']) / 2
                cy = (det['y1'] + det['y2']) / 2
                if fx <= cx <= fx + fw and fy <= cy <= fy + fh:
                    filtered_detections.append(det)
            detections = filtered_detections
            logger.info(f"Filtered to {len(detections)} lesions within face region.")
        
        # 3. Generate heatmap
        heatmap_url = self._generate_heatmap(image_path, detections, face_bbox)
        
        # Calculate real metrics based on detections
        lesion_count = len(detections)
        
        # Simple heuristic for severity score based on count and max confidence
        if lesion_count == 0:
            acne_score = 0.0
            severity_level = "Clear"
        else:
            # Score formula: base score from count, weighted by average confidence
            avg_conf = sum(d['confidence'] for d in detections) / lesion_count
            base_score = min(lesion_count * 5.0, 100.0) # Cap at 100
            acne_score = round(base_score * avg_conf, 1)
            
            if lesion_count < 5:
                severity_level = "Mild"
            elif lesion_count < 15:
                severity_level = "Moderate"
            else:
                severity_level = "Severe"
                
        return SkinAnalysisResult(
            skin_type=None,
            concerns=["Acne"] if lesion_count > 0 else [],
            hydration_level=None,
            acne=AcneReport(
                severity_score=acne_score,
                severity_level=severity_level,
                heatmap_url=heatmap_url,
                lesion_count=lesion_count
            )
        )
