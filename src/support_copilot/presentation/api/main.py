import logging
from time import perf_counter
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from support_copilot.application.use_cases.answer_support_question import AnswerSupportQuestion
from support_copilot.infrastructure.adapters.kb_chroma import ChromaKnowledgeRepository
from support_copilot.infrastructure.adapters.llm_openai import OpenAILLMProvider
from support_copilot.infrastructure.adapters.logs_elasticsearch import ElasticsearchLogProvider
from support_copilot.infrastructure.adapters.tickets_zendesk import ZendeskTicketProvider
from support_copilot.infrastructure.adapters.fallbacks import NullLogProvider, NullTicketProvider
from support_copilot.infrastructure.config.settings import settings
from support_copilot.infrastructure.observability.logging import configure_logging
from support_copilot.infrastructure.security.rate_limit import InMemoryRateLimiter

configure_logging(settings.log_level)
logger = logging.getLogger("support_copilot.api")
app = FastAPI(title=settings.app_name, version="1.0.0")
rate_limiter = InMemoryRateLimiter(max_requests=settings.rate_limit_per_minute, window_seconds=60)


class AskRequest(BaseModel):
    question: str = Field(min_length=5)


@app.middleware("http")
async def request_observability_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid4()))
    start = perf_counter()
    path = request.url.path

    if path != "/health":
        auth_header = request.headers.get("authorization", "")
        expected = f"Bearer {settings.api_auth_token}" if settings.api_auth_token else ""
        if settings.api_auth_token and auth_header != expected:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        client_ip = request.client.host if request.client else "unknown"
        if not rate_limiter.allow(client_ip):
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    response = await call_next(request)
    elapsed = round((perf_counter() - start) * 1000, 2)
    response.headers["x-request-id"] = request_id

    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "latency_ms": elapsed,
        },
    )
    return response


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
    result = use_case.execute(req.question)
    logger.info("copilot_answer_generated", extra={"timings_ms": result.get("timings_ms", {})})
    return result
