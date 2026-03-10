from typing import Any


class LLMClient:
    async def complete_structured(self, prompt: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    async def complete_structured(self, prompt: str, context: dict[str, Any]) -> dict[str, Any]:
        sources = context.get("sources", [])
        names = ", ".join(source["name"] for source in sources[:3]) or "nenhuma fonte"
        return {
            "answer": f"Análise baseada em fontes do LeanIX: {names}.",
            "sources": sources,
            "confidence": 0.84 if sources else 0.2,
            "mode": "read_only",
            "claim_type": "fact" if sources else "hypothesis",
        }
