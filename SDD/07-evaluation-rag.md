# 07. Evaluation RAG

## Objetivo

Medir qualidade das respostas RAG antes de promover mudanças para produção.

## Implementação

- Script: `evaluation/run_rag_eval.py`
- Dataset base: `evaluation/rag_eval_dataset.jsonl`
- Métricas:
  - `faithfulness`
  - `answer_relevancy`
  - `context_precision`

## Processo recomendado

1. Atualizar dataset com casos reais.
2. Rodar avaliação por release.
3. Comparar score com baseline.
4. Bloquear release quando regressão passar do limite.
