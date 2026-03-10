from fastapi import APIRouter, Depends

from app.api.dependencies import get_orchestration_service
from app.core.config import get_settings
from app.core.security import ensure_suggest_mode_allowed
from app.domain.schemas import EnrichmentSuggestRequest, EnrichmentSuggestResponse
from app.services.orchestration_service import OrchestrationService

router = APIRouter(tags=["suggest"])


@router.post("/suggest/enrichment", response_model=EnrichmentSuggestResponse)
async def suggest_enrichment(
    request: EnrichmentSuggestRequest,
    service: OrchestrationService = Depends(get_orchestration_service),
) -> EnrichmentSuggestResponse:
    ensure_suggest_mode_allowed(get_settings().enable_suggest_mode)
    result = await service.suggest_enrichment(request.fact_sheet_id)
    return EnrichmentSuggestResponse.model_validate(result)
