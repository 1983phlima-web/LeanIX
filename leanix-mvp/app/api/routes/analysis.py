from fastapi import APIRouter, Depends

from app.api.dependencies import get_orchestration_service
from app.domain.schemas import (
    GapAnalysisRequest,
    GapAnalysisResponse,
    ImpactAnalysisRequest,
    ImpactAnalysisResponse,
)
from app.services.orchestration_service import OrchestrationService

router = APIRouter(tags=["analysis"])


@router.post("/analysis/impact", response_model=ImpactAnalysisResponse)
async def analyze_impact(
    request: ImpactAnalysisRequest,
    service: OrchestrationService = Depends(get_orchestration_service),
) -> ImpactAnalysisResponse:
    result = await service.analyze_impact(request.application_name)
    return ImpactAnalysisResponse.model_validate(result)


@router.post("/analysis/gaps", response_model=GapAnalysisResponse)
async def analyze_gaps(
    request: GapAnalysisRequest,
    service: OrchestrationService = Depends(get_orchestration_service),
) -> GapAnalysisResponse:
    result = await service.analyze_gaps(request.fact_sheet_type)
    return GapAnalysisResponse.model_validate(result)
