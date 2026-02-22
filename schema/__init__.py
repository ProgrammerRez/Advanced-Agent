from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Tuple

# =========================
# STATE
# =========================

class ResearchState(BaseModel):
    topic: str
    mode: Literal["shallow", "deep"]
    groq_api_key: Optional[str] = None

    plan: List[str] = Field(default_factory=list)
    remaining_subtopics: List[str] = Field(default_factory=list)
    confidence_score: float = Field(default=0.9)

    extracted_notes: List[Tuple[str, str]] = Field(default_factory=list)
    validated_notes: List[str] = Field(default_factory=list)
    validated_sources: List[str] = Field(default_factory=list)

    depth: int = 0
    max_depth: int = 1

    final_report: Optional[str] = ""


# =========================
# STRUCTURED OUTPUT (Ineternal Nodes)
# =========================

class ResearchPlan(BaseModel):
    subtopics: List[str]
    depth_required: int
    requires_math: bool
    requires_sources: bool



# =========================
# Sybthesis Output (Internal Nodes)
# =========================

class SynthesisOutput(BaseModel):
    content: str
    confidence_score: float

    

# =========================
# API INPUT
# =========================

class APIInput(BaseModel):
    query: str
    mode: Literal['shallow','deep']
    groq_api_key: Optional[str] = None
    
