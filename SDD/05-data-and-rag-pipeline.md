# 05. Data and RAG Pipeline

## Fontes de dados

1. `knowledge_base/*.md`
2. tickets Zendesk
3. logs Elasticsearch

## Pipeline RAG

1. Carregar documentos Markdown.
2. Chunking (`RecursiveCharacterTextSplitter`).
3. Gerar embeddings.
4. Indexar no Chroma.
5. Recuperar top-k por similaridade.
6. Combinar com contexto operacional (tickets/logs).

## Estratégia de resposta

- síntese com contexto único,
- formato obrigatório:
  - DIAGNOSTICO
  - EVIDENCIAS
  - PROXIMOS_PASSOS.
