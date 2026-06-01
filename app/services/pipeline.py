import logging
import time
import os
import random
from PIL import Image, ImageDraw
from app.schemas.analysis import SkinAnalysisResult, AcneReport, Prediction, BoundingBox
from app.services.storage import save_image_locally

logger = logging.getLogger("glowup.pipeline")

# ==========================================
# Advanced ML Model Stubs
# ==========================================
class SkinSegmentationModel:
    def segment(self, image):
        logger.info("Running SkinSegmentationModel...")
        return "segmented_mask"

class SkinToneEstimator:
    def estimate(self, image):
        tones = ["Light", "Medium-Light", "Medium", "Medium-Dark", "Dark"]
        logger.info("Running SkinToneEstimator...")
        return Prediction(value=random.choice(tones), confidence=round(random.uniform(0.75, 0.99), 2))

class OilinessDrynessAnalyzer:
    def analyze(self, image):
        types = ["Oily", "Dry", "Combination", "Normal"]
        logger.info("Running OilinessDrynessAnalyzer...")
        return Prediction(value=random.choice(types), confidence=round(random.uniform(0.70, 0.95), 2))

class SensitivityRednessAnalyzer:
    def analyze(self, image):
        logger.info("Running SensitivityRednessAnalyzer...")
        return {"concerns": ["Redness"], "score": round(random.uniform(10.0, 80.0), 1)}

class QuestionnaireFusionModel:
    def fuse(self, visual_data, questionnaire_data=None):
        logger.info("Running QuestionnaireFusionModel...")
        return visual_data

# ==========================================
# Main Pipeline
# ==========================================
class SkinAnalysisPipeline:
    def __init__(self):
        logger.info("Initializing Skin Analysis Pipeline...")
        self.segmentation_model = SkinSegmentationModel()
        self.skin_tone_estimator = SkinToneEstimator()
        self.oil_dry_analyzer = OilinessDrynessAnalyzer()
        self.sensitivity_analyzer = SensitivityRednessAnalyzer()
        self.fusion_model = QuestionnaireFusionModel()
        
    def _generate_heatmap_and_boxes(self, image_path: str):
        """
        Simulates YOLOv8 by drawing hotspots and returning bounding boxes.
        Returns (heatmap_url, list_of_BoundingBox)
        """
        try:
            boxes = []
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                heatmap = img.copy()
                draw = ImageDraw.Draw(heatmap)
                width, height = img.size
                
                num_lesions = random.randint(2, 6)
                
                for _ in range(num_lesions):
                    x = random.randint(int(width * 0.2), int(width * 0.8))
                    y = random.randint(int(height * 0.2), int(height * 0.8))
                    r = random.randint(int(width * 0.02), int(width * 0.08))
                    
                    draw.ellipse((x - r, y - r, x + r, y + r), outline="red", width=max(1, int(width * 0.01)))
                    
                    boxes.append(BoundingBox(
                        x=x-r, y=y-r, width=r*2, height=r*2, 
                        confidence=round(random.uniform(0.60, 0.99), 2)
                    ))
                
                original_filename = os.path.basename(image_path)
                heatmap_filename = f"heatmap_{original_filename}"
                heatmap_path = save_image_locally(heatmap, heatmap_filename)
                
                return f"/uploads/{os.path.basename(heatmap_path)}", boxes
        except Exception as e:
            logger.error(f"Failed to generate heatmap: {e}")
            return "", []

    def analyze(self, image_path: str) -> SkinAnalysisResult:
        logger.info(f"Running full advanced pipeline on {image_path}")
        
        mask = self.segmentation_model.segment(image_path)
        skin_tone_pred = self.skin_tone_estimator.estimate(image_path)
        skin_type_pred = self.oil_dry_analyzer.analyze(image_path)
        sensitivity_data = self.sensitivity_analyzer.analyze(image_path)
        
        final_concerns = self.fusion_model.fuse(["Acne"] + sensitivity_data["concerns"])
        time.sleep(1)
        
        heatmap_url, lesions = self._generate_heatmap_and_boxes(image_path)
        
        acne_score = min(len(lesions) * 15.0 + random.uniform(0, 10), 100.0)
        severity_level = "Mild" if acne_score < 30 else "Moderate" if acne_score < 70 else "Severe"
        
        hydration_pred = Prediction(value=random.choice(["Low", "Medium", "High"]), confidence=round(random.uniform(0.6, 0.95), 2))
        
        return SkinAnalysisResult(
            skin_type=skin_type_pred,
            skin_tone=skin_tone_pred,
            hydration_level=hydration_pred,
            sensitivity_score=sensitivity_data["score"],
            concerns=final_concerns,
            acne=AcneReport(
                severity_score=round(acne_score, 1),
                severity_level=severity_level,
                heatmap_url=heatmap_url,
                lesion_count=len(lesions),
                lesions=lesions
            )
        )
