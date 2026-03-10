class RAGService:
    async def retrieve(self, question: str) -> list[dict[str, str]]:
        return [
            {
                "type": "rag_document",
                "id": "doc-001",
                "name": f"Padrão interno relacionado a: {question[:40]}",
            }
        ]
