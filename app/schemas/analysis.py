from pydantic import BaseModel
from typing import List, Optional

class Prediction(BaseModel):
    value: str
    confidence: float

class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int
    confidence: float

class AcneReport(BaseModel):
    severity_score: float
    severity_level: str
    heatmap_url: str
    lesion_count: int
    lesions: List[BoundingBox]

class SkinAnalysisResult(BaseModel):
    skin_type: Prediction
    skin_tone: Prediction
    hydration_level: Prediction
    sensitivity_score: float
    concerns: List[str]
    acne: AcneReport

class SkinAnalysisResponse(BaseModel):
    status: str
    message: str
    image_url: str
    analysis: SkinAnalysisResult
