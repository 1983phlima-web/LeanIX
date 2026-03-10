from fastapi import APIRouter, Depends

from app.api.dependencies import get_orchestration_service
from app.domain.schemas import FactsheetSearchRequest, FactsheetSearchResponse, FactsheetSummary
from app.services.orchestration_service import OrchestrationService

router = APIRouter(tags=["factsheets"])


@router.post("/factsheets/search", response_model=FactsheetSearchResponse)
async def search_factsheets(
    request: FactsheetSearchRequest,
    service: OrchestrationService = Depends(get_orchestration_service),
) -> FactsheetSearchResponse:
    items = await service.leanix_service.search_factsheets(request.fact_sheet_type, request.search_term)
    return FactsheetSearchResponse(
        results=[FactsheetSummary(id=item["id"], name=item["name"], type=item["type"]) for item in items]
    )
