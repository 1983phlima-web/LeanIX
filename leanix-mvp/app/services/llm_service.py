from app.clients.llm_client import LLMClient
from app.domain.models import QueryAnswer


class LLMService:
    def __init__(self, client: LLMClient):
        self.client = client

    async def answer(self, prompt: str, context: dict) -> QueryAnswer:
        raw = await self.client.complete_structured(prompt=prompt, context=context)
        return QueryAnswer.model_validate(raw)
