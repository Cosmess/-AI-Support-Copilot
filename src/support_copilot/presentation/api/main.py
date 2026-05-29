from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from support_copilot.application.use_cases.answer_support_question import AnswerSupportQuestion
from support_copilot.infrastructure.adapters.kb_chroma import ChromaKnowledgeRepository
from support_copilot.infrastructure.adapters.llm_openai import OpenAILLMProvider
from support_copilot.infrastructure.adapters.logs_elasticsearch import ElasticsearchLogProvider
from support_copilot.infrastructure.adapters.tickets_zendesk import ZendeskTicketProvider
from support_copilot.infrastructure.adapters.fallbacks import NullLogProvider, NullTicketProvider
from support_copilot.infrastructure.config.settings import settings

app = FastAPI(title=settings.app_name, version="1.0.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=5)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": settings.environment, "model": settings.openai_model}


@app.post("/ask")
def ask(req: AskRequest) -> dict:
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada")

    kb = ChromaKnowledgeRepository()
    llm = OpenAILLMProvider()

    try:
        logs = ElasticsearchLogProvider()
    except Exception:
        logs = NullLogProvider()

    try:
        tickets = ZendeskTicketProvider()
    except Exception:
        tickets = NullTicketProvider()

    use_case = AnswerSupportQuestion(kb=kb, tickets=tickets, logs=logs, llm=llm)
    return use_case.execute(req.question)
