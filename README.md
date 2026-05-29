# AI Support Copilot

Copiloto de suporte técnico com **Clean Architecture em Python**, **RAG**, integração com **Zendesk**, busca de **logs reais no Elasticsearch** e módulo de **avaliação RAG**.

Documentação de engenharia: `docs/` (pasta canônica). A pasta `SDD/` permanece apenas como legado/compatibilidade.

## Arquitetura

Este projeto foi estruturado no modelo **Ports and Adapters (Hexagonal/Clean Architecture)**:

- `domain`: entidades e contratos (ports)
- `application`: casos de uso (regras de orquestração)
- `infrastructure`: adapters externos (OpenAI, Chroma, Zendesk, Elasticsearch)
- `presentation`: API FastAPI

```text
src/support_copilot/
  domain/
    entities.py
    ports.py
  application/
    use_cases/
      answer_support_question.py
  infrastructure/
    adapters/
      kb_chroma.py
      llm_openai.py
      logs_elasticsearch.py
      tickets_zendesk.py
      fallbacks.py
    config/
      settings.py
  presentation/
    api/
      main.py
```

## Fluxo funcional

1. API recebe a pergunta (`/ask`)
2. Caso de uso consulta:
   - documentos via RAG (Chroma),
   - tickets no Zendesk,
   - logs no Elasticsearch.
3. LLM sintetiza:
   - diagnóstico,
   - evidências,
   - próximos passos.

## Subir com Docker Compose

1. Copie variáveis:

```bash
cp .env.example .env
```

2. Preencha no `.env`:
- `OPENAI_API_KEY`
- `ZENDESK_SUBDOMAIN`, `ZENDESK_EMAIL`, `ZENDESK_API_TOKEN` (opcional, mas recomendado)

3. Suba os serviços:

```bash
docker compose up --build -d
```

4. (Opcional) Seed de logs reais para teste:

```bash
python scripts/seed_elasticsearch_logs.py
```

5. Teste:

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Há backlog de webhook. Qual causa provável e prioridade?\"}"
```

## Avaliação RAG

Dataset inicial: `evaluation/rag_eval_dataset.jsonl`

Rodar avaliação:

```bash
python evaluation/run_rag_eval.py
```

Métricas calculadas com RAGAS:
- `faithfulness`
- `answer_relevancy`
- `context_precision`

## Execução local sem Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
uvicorn support_copilot.presentation.api.main:app --reload --port 8000
```

## Referências de arquitetura e integrações usadas

- FastAPI (project structure / bigger applications): https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Ports & Adapters em Python (Cosmic Python): https://www.cosmicpython.com/
- Zendesk Support API: https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/
- Elasticsearch Search API: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html
- RAGAS: https://docs.ragas.io/
