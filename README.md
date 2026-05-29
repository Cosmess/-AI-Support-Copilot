# AI Support Copilot

Copiloto técnico de suporte com **RAG + ReAct Agent + LangGraph**.

Ele recebe perguntas operacionais, busca contexto em base de conhecimento, investiga com tools (tickets/logs/prioridade) e retorna:

1. Diagnóstico provável
2. Evidências
3. Próximos passos

## Arquitetura

- **FastAPI**: endpoint `/ask`
- **RAG**: Markdown -> chunking -> embeddings -> Chroma
- **Agent ReAct**: ferramentas para investigação simulada
- **LangGraph**: fluxo `retrieve_context -> investigate_with_agent -> generate_answer`

## Estrutura

```text
app/
  agent.py
  config.py
  knowledge_base.py
  main.py
  pipeline.py
  tools.py
knowledge_base/
  runbooks.md
  support_policies.md
```

## Requisitos

- Python 3.11+
- OPENAI_API_KEY

## Como executar

1. Criar ambiente virtual e instalar dependências:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

2. Configurar variáveis:

```bash
copy .env.example .env
```

Preencha `OPENAI_API_KEY` no `.env`.

3. Subir API:

```bash
uvicorn app.main:app --reload --port 8000
```

4. Testar:

```bash
curl -X POST "http://127.0.0.1:8000/ask" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"Investigue o incidente INC-1003 e diga a prioridade\"}"
```

## Exemplo de retorno esperado

```json
{
  "question": "Investigue o incidente INC-1003 e diga a prioridade",
  "answer": "Diagnóstico provável ... Evidências ... Próximos passos ...",
  "retrieved_context": "...",
  "agent_output": "..."
}
```

## Próximas evoluções

- Integrar logs reais (Elastic/OpenSearch)
- Integrar tickets reais (Jira/Zendesk)
- Trocar Chroma por pgvector
- Adicionar testes automatizados e avaliação RAG
