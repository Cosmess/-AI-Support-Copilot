# 11. Risk Register

## Riscos técnicos

1. **Dependência de APIs externas**  
   Impacto: respostas incompletas.  
   Mitigação: fallbacks, retry, circuit breaker.

2. **Qualidade de contexto RAG insuficiente**  
   Impacto: diagnóstico fraco.  
   Mitigação: tuning de chunking, reranking, dataset de avaliação.

3. **Custos de LLM**  
   Impacto: inviabilidade financeira.  
   Mitigação: cache, modelos menores para rotas não críticas.

4. **Vazamento de dados sensíveis**  
   Impacto: risco de compliance.  
   Mitigação: mascaramento e políticas de acesso.
