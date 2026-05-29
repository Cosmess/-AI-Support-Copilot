# 08. Observability and Operations

## Observabilidade mínima

1. logs de aplicação por requisição.
2. latência total por endpoint.
3. tempo de cada dependência externa:
   - Zendesk,
   - Elasticsearch,
   - LLM.

## Operação local

1. `docker compose up --build -d`
2. seed de logs: `python scripts/seed_elasticsearch_logs.py`
3. teste API `/ask`

## Operação em produção (recomendado)

1. health-checks automatizados.
2. alertas para timeout/erro em integrações.
3. rastreio de custo de tokens.
