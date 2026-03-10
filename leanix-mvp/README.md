# LeanIX Architect Copilot MVP

MVP em Python/FastAPI para consulta arquitetural sobre SAP LeanIX com modo **read-only** por padrão, respostas estruturadas, fontes explícitas e guardrails simples.

## O que este projeto entrega

- API FastAPI com endpoints principais
- Cliente GraphQL para LeanIX
- Orquestração de consulta + RAG opcional + LLM mockado
- Policy engine simples para bloquear saídas sem fonte
- Testes básicos
- Dockerfile e docker-compose
- `.env.example`

## Estrutura

```text
app/
  api/
    dependencies.py
    routes/
      analysis.py
      factsheets.py
      health.py
      query.py
      suggest.py
  clients/
    leanix_graphql_client.py
    llm_client.py
  core/
    config.py
    logging.py
    security.py
  domain/
    models.py
    policies.py
    schemas.py
  prompts/
    query_prompt.py
  services/
    leanix_service.py
    llm_service.py
    orchestration_service.py
    rag_service.py
  tests/
    test_api.py
    test_orchestration_service.py
    test_policy_engine.py
  main.py
```

## Endpoints

- `GET /api/v1/health`
- `POST /api/v1/query`
- `POST /api/v1/factsheets/search`
- `POST /api/v1/analysis/impact`
- `POST /api/v1/analysis/gaps`
- `POST /api/v1/suggest/enrichment`

## Setup local

1. Crie um ambiente virtual.
2. Instale as dependências.
3. Copie `.env.example` para `.env`.
4. Ajuste `LEANIX_BASE_URL` e `LEANIX_API_TOKEN`.
5. Rode a aplicação.

### Comandos

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload
```

## Rodando com Docker

```bash
docker compose up --build
```

## Exemplo de chamada

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quais aplicações suportam Customer Service e apresentam risco de obsolescência?",
    "include_sources": true
  }'
```

## Exemplo de GraphQL para LeanIX

```graphql
query SearchApplications($factSheetType: FactSheetType!, $searchTerm: String) {
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
```

## Boas práticas já embutidas

- separação entre API, domínio, serviços e clientes
- feature flag para `suggest mode`
- timeout e retry no client LeanIX
- validação por Pydantic
- política para bloquear resposta sem fonte
- tipagem e testes iniciais

## Limitações da MVP

- o LLM está mockado
- o parser de intenção é simples
- o RAG é apenas ilustrativo
- não há write-back real no LeanIX
- não há autenticação de usuários finais

## Roadmap v2

- plugar provedor real de LLM
- adicionar cache de contexto
- enriquecer consultas GraphQL por tipo de factsheet
- adicionar ranking de confiança por cobertura de fontes
- criar workflow de aprovação para sugestões
- integrar OpenTelemetry e métricas
