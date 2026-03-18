from pydantic import BaseModel
from typing import List

class AnalysisResponse(BaseModel):
    company:str
    event_summary:List[str]
    event_type:str
    impact_direction:str
    reasoning_chain:List[str]
    risks: List[str]
    confidence:str