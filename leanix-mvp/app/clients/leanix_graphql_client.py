from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import Settings


class LeanIXGraphQLClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=4))
    async def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.settings.leanix_api_token}",
            "Content-Type": "application/json",
        }
        payload = {"query": query, "variables": variables or {}}
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(self.settings.leanix_base_url, headers=headers, json=payload)
            response.raise_for_status()
            body = response.json()
            if "errors" in body:
                raise RuntimeError(f"Erro GraphQL LeanIX: {body['errors']}")
            return body["data"]
