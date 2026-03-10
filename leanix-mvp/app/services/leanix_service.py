from typing import Any

from app.clients.leanix_graphql_client import LeanIXGraphQLClient

FACTSHEET_SEARCH_QUERY = """
query SearchFactSheets($factSheetType: FactSheetType!, $searchTerm: String) {
  allFactSheets(factSheetType: $factSheetType, searchTerm: $searchTerm, first: 10) {
    edges {
      node {
        id
        name
        type
      }
    }
  }
}
"""


class LeanIXService:
    def __init__(self, client: LeanIXGraphQLClient):
        self.client = client

    async def search_factsheets(self, fact_sheet_type: str, search_term: str | None = None) -> list[dict[str, str]]:
        data = await self.client.execute(
            FACTSHEET_SEARCH_QUERY,
            variables={"factSheetType": fact_sheet_type, "searchTerm": search_term},
        )
        edges = data.get("allFactSheets", {}).get("edges", [])
        return [edge["node"] for edge in edges]

    async def fetch_context_for_question(self, question: str) -> dict[str, Any]:
        guessed_type = "Application"
        search_term = self._extract_search_term(question)
        factsheets = await self.search_factsheets(guessed_type, search_term)
        sources = [
            {"type": "leanix_factsheet", "id": item["id"], "name": item["name"]}
            for item in factsheets
        ]
        return {"question": question, "factsheets": factsheets, "sources": sources}

    @staticmethod
    def _extract_search_term(question: str) -> str | None:
        tokens = [token.strip("?,.") for token in question.split() if len(token) > 4]
        return tokens[-1] if tokens else None
