# Incident Runbook

## Objetivo
Padronizar investigação de incidentes no copiloto.

## Passos
1. Validar impacto e urgência.
2. Coletar tickets relacionados (Zendesk).
3. Coletar logs recentes (Elasticsearch).
4. Consultar políticas/runbooks via RAG.
5. Emitir diagnóstico + evidências + próximos passos.

## Escalonamento
- Escalar para humano quando:
  - não há evidência suficiente,
  - conflito entre fontes,
  - impacto crítico sem workaround.
