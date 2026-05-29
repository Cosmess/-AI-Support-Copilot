# 01. Product Requirements

## Contexto

Criar um copiloto técnico para suporte com foco em investigação operacional usando IA.

## Requisitos funcionais

1. Responder perguntas técnicas de suporte.
2. Buscar contexto em base de conhecimento (RAG).
3. Consultar tickets reais no Zendesk.
4. Consultar logs reais no Elasticsearch.
5. Gerar saída com:
   - diagnóstico provável,
   - evidências,
   - próximos passos.
6. Disponibilizar API HTTP para consumo.
7. Fornecer avaliação de qualidade RAG.

## Requisitos não funcionais

1. Arquitetura limpa (separação clara de domínio/aplicação/infra/apresentação).
2. Deploy via Docker Compose.
3. Configuração por variáveis de ambiente.
4. Observabilidade mínima para operação.
5. Segurança básica de segredos e dados.
