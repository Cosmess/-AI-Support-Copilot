# ADR-0002: Start RAG with Chroma

## Status
Accepted

## Context
Era necessário iniciar com baixo atrito operacional e custo de setup.

## Decision
Usar Chroma como primeiro vetor store local, mantendo contrato de repositório para troca futura (pgvector/Pinecone).

## Consequences
- Setup rápido para desenvolvimento.
- Migração futura facilitada por abstração de porta.
