from enum import Enum

from pydantic import BaseModel, Field


class ClaimType(str, Enum):
    FACT = "fact"
    SUGGESTION = "suggestion"
    HYPOTHESIS = "hypothesis"


class SourceType(str, Enum):
    LEANIX_FACTSHEET = "leanix_factsheet"
    RAG_DOCUMENT = "rag_document"


class SourceRef(BaseModel):
    type: SourceType
    id: str
    name: str
    url: str | None = None


class QueryAnswer(BaseModel):
    answer: str
    sources: list[SourceRef] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    mode: str = "read_only"
    claim_type: ClaimType = ClaimType.FACT
