# 09. Security and Compliance

## Segredos

- usar `.env` local e secret manager em produção.
- nunca versionar tokens/chaves.

## Dados sensíveis

1. reduzir exposição de PII em logs.
2. limitar campos retornados de tickets.
3. adicionar política de retenção de dados.

## Acesso

1. permissões mínimas em Zendesk API.
2. permissões mínimas no Elasticsearch.
3. criptografia em trânsito (HTTPS/TLS) em produção.
