from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.config import settings
from app.pipeline import run_copilot


class AskRequest(BaseModel):
    question: str = Field(min_length=5, description="Pergunta de suporte técnico")


class AskResponse(BaseModel):
    question: str
    answer: str
    retrieved_context: str
    agent_output: str


app = FastAPI(title="AI Support Copilot", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": settings.openai_model}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada")

    result = run_copilot(req.question)
    return AskResponse(
        question=req.question,
        answer=result["final_answer"],
        retrieved_context=result["context"],
        agent_output=result["agent_output"],
    )
