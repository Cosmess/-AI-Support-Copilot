# 02. System Architecture

## Arquitetura lógica (AI-First)

1. **API Layer**: recebe pergunta via `/ask`.
2. **Use Case Layer**: orquestra coleta de contexto e síntese.
3. **Knowledge Layer (RAG)**: recuperação vetorial de documentos.
4. **Operational Data Layer**:
   - Zendesk (tickets),
   - Elasticsearch (logs).
5. **LLM Layer**: síntese final com formato padronizado.
6. **Evaluation Layer**: mede qualidade RAG com RAGAS.

## Fluxo ponta a ponta

1. Pergunta do usuário.
2. Recuperação de documentos da base.
3. Busca de tickets relevantes.
4. Busca de logs relevantes.
5. Montagem de prompt estruturado.
6. Geração da resposta final.
7. Retorno de artefatos de evidência.
