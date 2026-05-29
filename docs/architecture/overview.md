# Architecture Overview

Arquitetura Clean/Hexagonal:

- `domain`: entidades e portas
- `application`: casos de uso
- `infrastructure`: adapters externos
- `presentation`: API FastAPI

Fluxo:
1. Pergunta entra em `/ask`
2. Recupera contexto (RAG + Zendesk + logs)
3. LLM sintetiza resposta estruturada
4. Retorno com evidências
