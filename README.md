# LeanIX
Aplicação LLM para permitir que um usuário pergunte em linguagem natural sobre o landscape arquitetural e receba respostas baseadas em dados do LeanIX, com evidência e explicação estruturada.
MVP técnica de um Copiloto Arquitetural para SAP LeanIX, usando boas práticas de desenvolvimento, segurança, observabilidade e separação de responsabilidades.

# META
A aplicação deve permitir que um usuário faça perguntas em linguagem natural sobre o landscape arquitetural e receba respostas baseadas em dados do LeanIX, com evidência e explicação estruturada.

# ESCOPO
Implementar uma solução com os seguintes componentes:
Backend API em Python com FastAPI
Conector LeanIX via GraphQL
Camada RAG opcional com documentos locais
Integração com LLM
Policy engine simples para validar respostas e bloquear write-back indevido
Observabilidade com logs estruturados
Testes unitários e de integração
Docker e docker-compose
Modo read-only por padrão
Modo suggest-update opcional, sem gravar no LeanIX automaticamente

# STACK
Python 3.12

FastAPI

httpx

pydantic v2

uvicorn

structlog ou loguru

pytest

python-dotenv

tenacity para retry

LangChain apenas se realmente necessário e preferir implementação simples e explícita

OpenAI SDK ou interface abstrata de LLM provider

FAISS ou Chroma para vetor store local

Docker

Ruff + Black + mypy

# REQUISITOS
Criar os endpoints:
GET /health
POST /query
POST /factsheets/search
POST /analysis/impact
POST /analysis/gaps
POST /suggest/enrichment

# ENDPOINT/QUERY
Entrada: JSON
{
  "question": "Quais aplicações suportam a capability Customer Service e possuem tecnologia em fim de vida?",
  "include_sources": true
}

Saída:
{
  "answer": "texto objetivo e técnico",
  "sources": [{"type": "leanix_factsheet","id": "fs_123", "name": "Application A"}],
  "confidence": 0.84,
  "mode": "read_only"
}

# ARQUITETURA
Implementar a solução seguindo esta estrutura:
app/
  api/
    routes/
  core/
    config.py
    logging.py
    security.py
  domain/
    models.py
    schemas.py
    policies.py
  services/
    leanix_service.py
    rag_service.py
    llm_service.py
    orchestration_service.py
  clients/
    leanix_graphql_client.py
    llm_client.py
  tests/
  main.py

# RULES
Não acoplar lógica de negócio aos controllers
Usar dependency injection simples
Criar interfaces claras para LLM e LeanIX client
Isolar prompts em arquivos ou constantes versionáveis
Toda resposta do LLM deve passar por validação de schema
Toda resposta deve informar fontes
Não permitir write-back automático no LeanIX
Criar um feature flag ENABLE_SUGGEST_MODE
Implementar timeout, retry e tratamento de erro nas chamadas externas
Implementar logs com correlation_id por requisição
Não hardcodar tokens
Usar variáveis de ambiente com .env.example
Requisitos de integração com LeanIX
Criar um cliente GraphQL genérico com autenticação por token
função para executar queries GraphQL
função para buscar factsheets por tipo
função para recuperar relações básicas
função para buscar factsheets por filtro simples
Criar exemplos de queries GraphQL para:
Application
Business Capability
Tech Category ou Technology
Relações entre factsheets
Requisitos de IA
Implementar uma camada de orquestração com este fluxo:
interpretar a pergunta
mapear intenção
buscar dados no LeanIX
opcionalmente enriquecer via RAG
montar prompt estruturado
pedir resposta ao LLM
validar resposta em schema pydantic
retornar resultado com fontes

# GUARDRAILS
Se não houver evidência suficiente, responder explicitamente que faltam dados
Nunca inventar factsheets
Nunca inferir relações não retornadas pela API sem marcar como hipótese
Nunca retornar saída sem campo sources
Toda sugestão deve ser classificada como suggestion, fact ou hypothesis

# TESTES

-Criar:
testes unitários para os services
mock do LeanIX GraphQL client
mock do LLM client
testes para policy engine
teste de integração do endpoint /query
Requisitos de documentação

-Gerar:
README.md completo
instruções de setup local
instruções de configuração do token do LeanIX
instruções de execução com Docker
exemplos de chamadas curl
limitações atuais da MVP
roadmap da versão 2
Entregáveis esperados
código completo do projeto
estrutura de diretórios
arquivos Docker
.env.example
testes

# DIRECIONAMENTO TÉCNICO

Eu seguiria a MVP assim:

**Fase 1**
- FastAPI
- cliente LeanIX GraphQL
- endpoint `/query`
- resposta com fontes
- modo read-only
  
**Fase 2**
- RAG local com ADRs e padrões
- análise de gaps
- score de confiança
  
**Fase 3**
- sugestões de enriquecimento
- fila de aprovação
- write-back governado

## CORE DA MVP

Para visualizar o núcleo da orquestração:

class OrchestrationService:
    def __init__(self, leanix_service, rag_service, llm_service, policy_engine):
        self.leanix_service = leanix_service
        self.rag_service = rag_service
        self.llm_service = llm_service
        self.policy_engine = policy_engine

    async def answer_question(self, question: str) -> dict:
        intent = self._infer_intent(question)
        leanix_context = await self.leanix_service.fetch_context(intent, question)
        rag_context = await self.rag_service.retrieve(question)

        prompt = self._build_prompt(
            question=question,
            leanix_context=leanix_context,
            rag_context=rag_context,
        )

        raw_response = await self.llm_service.generate_structured(prompt)
        validated = self.policy_engine.validate(raw_response, leanix_context)

        return validated

# RESSALVAS
GraphQL do LeanIX varia conforme tenant, schema e versão do workspace, então a query exemplo pode precisar de ajuste fino no seu ambiente real
O LLM está mockado de propósito, para a MVP nascer controlada e previsível
O RAG está ilustrativo, não produtivo então agora baixe o pacote e plugue um provedor real de LLM e refinar as queries GraphQL com o seu metamodelo LeanIX.
Baixe o pacote e use o README, Enjoy  []'s
