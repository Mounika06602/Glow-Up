from pydantic import BaseModel
from typing import List, Optional

class AcneReport(BaseModel):
    severity_score: float
    severity_level: str
    heatmap_url: str
    lesion_count: int

class SkinAnalysisResult(BaseModel):
    skin_type: Optional[str] = None
    concerns: List[str]
    hydration_level: Optional[str] = None
    acne: AcneReport

class SkinAnalysisResponse(BaseModel):
    status: str
    message: str
    image_url: str
    analysis: SkinAnalysisResult
