import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import logging
import os
import urllib.request
from typing import Tuple, List, Optional, Dict, Any
from ultralytics import YOLO
from app.core.config import settings

logger = logging.getLogger("glowup.ml")

class FaceDetector:
    def __init__(self):
        logger.info("Initializing FaceDetector...")
        self.mp_face_detector = None
        
        # Initialize MediaPipe Tasks API Face Detection
        model_dir = settings.MODEL_DIR
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, 'blaze_face_short_range.tflite')
        
        # Download model if it doesn't exist
        if not os.path.exists(model_path):
            logger.info("Downloading MediaPipe Face Detection model...")
            url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
            try:
                urllib.request.urlretrieve(url, model_path)
                logger.info("Downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download MediaPipe model: {e}")
        
        if os.path.exists(model_path):
            try:
                base_options = python.BaseOptions(model_asset_path=model_path)
                options = vision.FaceDetectorOptions(base_options=base_options, min_detection_confidence=0.5)
                self.mp_face_detector = vision.FaceDetector.create_from_options(options)
            except Exception as e:
                logger.error(f"Failed to initialize MediaPipe FaceDetector: {e}")
                
        # Initialize OpenCV Haar Cascade Fallback
        haar_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(haar_cascade_path)
        
        if self.face_cascade.empty():
            logger.error("Failed to load Haar cascade for face detection.")

    def detect_face(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detects a face in the image using MediaPipe, falling back to Haar cascade.
        Returns the bounding box (x, y, w, h) or None if no face is found.
        """
        ih, iw, _ = image.shape
        
        # 1. Try MediaPipe first
        if self.mp_face_detector is not None:
            try:
                # MediaPipe expects RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
                
                results = self.mp_face_detector.detect(mp_image)
                
                if results.detections:
                    # We assume the first detected face is the target
                    detection = results.detections[0]
                    bbox = detection.bounding_box
                    
                    x = int(bbox.origin_x)
                    y = int(bbox.origin_y)
                    w = int(bbox.width)
                    h = int(bbox.height)
                    
                    # Ensure coordinates are within image boundaries
                    x = max(0, x)
                    y = max(0, y)
                    w = min(w, iw - x)
                    h = min(h, ih - y)
                    
                    logger.info("Face detected using MediaPipe.")
                    return (x, y, w, h)
            except Exception as e:
                logger.error(f"MediaPipe detection failed: {e}")
                
        logger.warning("MediaPipe failed to detect face or is not initialized. Falling back to Haar Cascade.")
        
        # 2. Fallback to OpenCV Haar Cascade
        # Haar cascade expects grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Adjust parameters for better detection if needed
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) > 0:
            # Return the first face found
            x, y, w, h = faces[0]
            logger.info("Face detected using OpenCV Haar Cascade.")
            return (int(x), int(y), int(w), int(h))
            
        logger.error("No face detected by either MediaPipe or Haar Cascade.")
        return None

class AcneDetector:
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = settings.YOLO_MODEL_PATH
            
        logger.info(f"Initializing AcneDetector with model: {model_path}...")
        try:
            # The ultralytics library handles both YOLOv8 and YOLOv9 based on the weights file
            # It will auto-download yolov8n.pt if it doesn't exist locally
            self.model = YOLO(model_path)
            logger.info("YOLO model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            self.model = None

    def detect(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Runs YOLO inference on the given image.
        Returns a list of dictionaries containing bounding boxes and confidences.
        """
        if self.model is None:
            logger.error("YOLO model is not loaded. Cannot perform inference.")
            return []
            
        try:
            # Run inference
            # We can adjust conf (confidence threshold) and iou (NMS threshold)
            results = self.model(image, conf=0.25, iou=0.45)
            
            detections = []
            
            # results is a list of Results objects, usually one per image
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding box coordinates in xyxy format
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0].cpu().numpy())
                    cls_id = int(box.cls[0].cpu().numpy())
                    
                    detections.append({
                        "x1": int(x1),
                        "y1": int(y1),
                        "x2": int(x2),
                        "y2": int(y2),
                        "confidence": conf,
                        "class_id": cls_id
                    })
                    
            logger.info(f"YOLO inference completed. Found {len(detections)} lesions.")
            return detections
            
        except Exception as e:
            logger.error(f"Error during YOLO inference: {e}")
            return []
