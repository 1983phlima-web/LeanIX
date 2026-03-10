from app.clients.llm_client import MockLLMClient
from app.domain.policies import PolicyEngine
from app.services.leanix_service import LeanIXService
from app.services.llm_service import LLMService
from app.services.orchestration_service import OrchestrationService
from app.services.rag_service import RAGService


class FakeLeanIXClient:
    async def execute(self, query: str, variables: dict | None = None) -> dict:
        return {
            "allFactSheets": {
                "edges": [
                    {"node": {"id": "fs-1", "name": "CRM Core", "type": "Application"}},
                    {"node": {"id": "fs-2", "name": "Portal CX", "type": "Application"}},
                ]
            }
        }


async def test_answer_question_returns_sources() -> None:
    service = OrchestrationService(
        leanix_service=LeanIXService(FakeLeanIXClient()),
        rag_service=RAGService(),
        llm_service=LLMService(MockLLMClient()),
        policy_engine=PolicyEngine(),
    )
    result = await service.answer_question("Quais apps suportam customer service?")
    assert result.sources
    assert result.confidence > 0.5
