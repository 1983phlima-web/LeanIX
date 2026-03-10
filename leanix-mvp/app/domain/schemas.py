from pydantic import BaseModel, Field

from app.domain.models import QueryAnswer, SourceRef


class HealthResponse(BaseModel):
    status: str = "ok"


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    include_sources: bool = True


class QueryResponse(QueryAnswer):
    pass


class FactsheetSearchRequest(BaseModel):
    fact_sheet_type: str = Field(alias="factSheetType")
    search_term: str | None = None
    limit: int = Field(default=10, ge=1, le=50)


class FactsheetSummary(BaseModel):
    id: str
    name: str
    type: str


class FactsheetSearchResponse(BaseModel):
    results: list[FactsheetSummary]


class ImpactAnalysisRequest(BaseModel):
    application_name: str


class ImpactAnalysisResponse(BaseModel):
    application_name: str
    impacted_relations: list[SourceRef]
    summary: str


class GapAnalysisRequest(BaseModel):
    fact_sheet_type: str


class GapAnalysisResponse(BaseModel):
    summary: str
    missing_fields_examples: list[str]


class EnrichmentSuggestRequest(BaseModel):
    fact_sheet_id: str


class EnrichmentSuggestResponse(BaseModel):
    fact_sheet_id: str
    proposed_description: str
    tags: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
