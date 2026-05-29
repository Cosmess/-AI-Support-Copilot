# 10. DevEx and Delivery

## Setup

1. criar `.env` a partir de `.env.example`
2. subir stack com docker compose
3. validar `/health` e `/ask`

## Convenções de engenharia

1. casos de uso no `application`.
2. adapters externos no `infrastructure`.
3. domínio sem dependência de framework.

## Entrega contínua (recomendado)

1. lint + testes + avaliação RAG em CI.
2. versionamento semântico.
3. changelog por release.
