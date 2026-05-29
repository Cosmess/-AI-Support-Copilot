from support_copilot.application.use_cases.answer_support_question import AnswerSupportQuestion
from support_copilot.domain.entities import RetrievedDocument, TicketEvent, LogEvent


class FakeKB:
    def retrieve(self, question: str, k: int = 4):
        return [
            RetrievedDocument(source="kb/runbooks.md", content="Webhook com backlog exige validar consumidor."),
            RetrievedDocument(source="kb/policies.md", content="P1 quando há indisponibilidade total."),
        ]


class FakeTickets:
    def find_by_query(self, query: str, limit: int = 3):
        return [
            TicketEvent(
                ticket_id="1001",
                status="open",
                priority="high",
                subject="Webhook timeout",
                description="Eventos parados",
                tags=["webhook", "timeout"],
            )
        ]


class FakeLogs:
    def search(self, query: str, limit: int = 10):
        return [
            LogEvent(
                timestamp="2026-05-29T15:00:00Z",
                service="webhook-worker",
                level="ERROR",
                message="Backlog increasing in webhook queue",
            )
        ]


class FakeLLM:
    def answer(self, prompt: str) -> str:
        return """DIAGNOSTICO:
Fila de webhook sem consumo está causando atraso.
EVIDENCIAS:
- Ticket 1001 aberto sobre timeout.
- Logs mostram backlog crescente.
PROXIMOS_PASSOS:
- Reiniciar consumidor.
- Reprocessar mensagens DLQ.
"""


def test_answer_support_question_returns_structured_payload():
    use_case = AnswerSupportQuestion(kb=FakeKB(), tickets=FakeTickets(), logs=FakeLogs(), llm=FakeLLM())
    result = use_case.execute("Há backlog de webhook, o que fazer?")

    assert result["question"]
    assert result["answer"]["diagnosis"] == "Fila de webhook sem consumo está causando atraso."
    assert len(result["answer"]["evidence"]) == 2
    assert "Reiniciar consumidor." in result["answer"]["next_steps"]
    assert len(result["retrieved_context"]) >= 1
