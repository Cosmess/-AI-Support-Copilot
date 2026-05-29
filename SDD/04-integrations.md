# 04. Integrations

## Zendesk

- Adapter: `infrastructure/adapters/tickets_zendesk.py`
- Endpoint utilizado: `GET /api/v2/search.json`
- Auth: `email/token` + `api_token`
- Saída: `ticket_id`, `status`, `priority`, `subject`, `description`, `tags`

## Elasticsearch

- Adapter: `infrastructure/adapters/logs_elasticsearch.py`
- Operação: `search` por `message` e `service`
- Índice padrão: `support-logs`
- Saída: `@timestamp`, `service`, `level`, `message`

## OpenAI

- Adapter: `infrastructure/adapters/llm_openai.py`
- Uso:
  - embeddings para recuperação vetorial
  - geração final de resposta
