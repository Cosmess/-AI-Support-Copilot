# ADR-0001: Use Clean Architecture

## Status
Accepted

## Context
O projeto precisa evoluir integrações sem acoplamento ao framework/fornecedor.

## Decision
Adotar Clean Architecture (Ports & Adapters) com separação em `domain`, `application`, `infrastructure`, `presentation`.

## Consequences
- Melhor testabilidade e manutenção.
- Maior disciplina de boundary entre camadas.
