from fastapi import APIRouter, Depends

from app.api.dependencies import get_orchestration_service
from app.domain.schemas import QueryRequest, QueryResponse
from app.services.orchestration_service import OrchestrationService

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    service: OrchestrationService = Depends(get_orchestration_service),
) -> QueryResponse:
    result = await service.answer_question(request.question)
    return QueryResponse.model_validate(result.model_dump())
