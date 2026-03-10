from app.clients.leanix_graphql_client import LeanIXGraphQLClient
from app.clients.llm_client import MockLLMClient
from app.core.config import get_settings
from app.domain.policies import PolicyEngine
from app.services.leanix_service import LeanIXService
from app.services.llm_service import LLMService
from app.services.orchestration_service import OrchestrationService
from app.services.rag_service import RAGService


def get_orchestration_service() -> OrchestrationService:
    settings = get_settings()
    leanix_client = LeanIXGraphQLClient(settings)
    leanix_service = LeanIXService(leanix_client)
    rag_service = RAGService()
    llm_service = LLMService(MockLLMClient())
    policy_engine = PolicyEngine()
    return OrchestrationService(leanix_service, rag_service, llm_service, policy_engine)
