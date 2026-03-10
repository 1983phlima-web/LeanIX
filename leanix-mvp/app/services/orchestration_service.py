from app.domain.models import QueryAnswer, SourceRef, SourceType
from app.domain.policies import PolicyEngine
from app.prompts.query_prompt import QUERY_PROMPT
from app.services.leanix_service import LeanIXService
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService


class OrchestrationService:
    def __init__(
        self,
        leanix_service: LeanIXService,
        rag_service: RAGService,
        llm_service: LLMService,
        policy_engine: PolicyEngine,
    ):
        self.leanix_service = leanix_service
        self.rag_service = rag_service
        self.llm_service = llm_service
        self.policy_engine = policy_engine

    async def answer_question(self, question: str) -> QueryAnswer:
        leanix_context = await self.leanix_service.fetch_context_for_question(question)
        rag_context = await self.rag_service.retrieve(question)
        all_sources = list(leanix_context["sources"])
        all_sources.extend(rag_context)

        prompt = QUERY_PROMPT.format(question=question)
        answer = await self.llm_service.answer(prompt, {"sources": all_sources})

        normalized_sources = [
            SourceRef(
                type=SourceType(source["type"]),
                id=source["id"],
                name=source["name"],
                url=source.get("url"),
            )
            for source in all_sources
        ]
        answer.sources = normalized_sources
        return self.policy_engine.validate_answer(answer)

    async def analyze_impact(self, application_name: str) -> dict:
        context = await self.leanix_service.fetch_context_for_question(application_name)
        return {
            "application_name": application_name,
            "impacted_relations": [
                SourceRef(type=SourceType.LEANIX_FACTSHEET, id=s["id"], name=s["name"])
                for s in context["sources"]
            ],
            "summary": f"Possíveis impactos identificados para {application_name} em relações retornadas pelo LeanIX.",
        }

    async def analyze_gaps(self, fact_sheet_type: str) -> dict:
        return {
            "summary": f"Análise inicial de gaps para {fact_sheet_type}.",
            "missing_fields_examples": ["description", "lifecycle", "owner"],
        }

    async def suggest_enrichment(self, fact_sheet_id: str) -> dict:
        return {
            "fact_sheet_id": fact_sheet_id,
            "proposed_description": "Descrição sugerida com base em contexto arquitetural e padrões internos.",
            "tags": ["candidate", "ai-enriched"],
            "confidence": 0.78,
        }
