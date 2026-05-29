from dataclasses import dataclass
from typing import List
from time import perf_counter
from support_copilot.domain.entities import CopilotAnswer
from support_copilot.domain.ports import KnowledgeRepository, TicketProvider, LogProvider, LLMProvider


@dataclass
class AnswerSupportQuestion:
    kb: KnowledgeRepository
    tickets: TicketProvider
    logs: LogProvider
    llm: LLMProvider

    def execute(self, question: str) -> dict:
        t0 = perf_counter()
        docs = self.kb.retrieve(question, k=4)
        t1 = perf_counter()
        ticket_events = self.tickets.find_by_query(query=question, limit=3)
        t2 = perf_counter()
        log_events = self.logs.search(query=question, limit=12)
        t3 = perf_counter()

        context = self._build_context(docs, ticket_events, log_events)
        prompt = self._build_prompt(question, context)
        raw = self.llm.answer(prompt)
        t4 = perf_counter()
        parsed = self._parse_answer(raw)

        return {
            "question": question,
            "answer": {
                "diagnosis": parsed.diagnosis,
                "evidence": parsed.evidence,
                "next_steps": parsed.next_steps,
                "raw_response": parsed.raw_response,
            },
            "retrieved_context": [f"{d.source}: {d.content[:220]}" for d in docs],
            "tickets": [t.__dict__ for t in ticket_events],
            "logs": [l.__dict__ for l in log_events[:8]],
            "timings_ms": {
                "rag_retrieval": round((t1 - t0) * 1000, 2),
                "zendesk_lookup": round((t2 - t1) * 1000, 2),
                "log_lookup": round((t3 - t2) * 1000, 2),
                "llm_generation": round((t4 - t3) * 1000, 2),
                "total": round((t4 - t0) * 1000, 2),
            },
        }

    @staticmethod
    def _build_context(docs, tickets, logs) -> str:
        docs_part = "\n".join(f"- [{d.source}] {d.content[:600]}" for d in docs) or "- sem documentos relevantes"
        tickets_part = "\n".join(
            f"- {t.ticket_id} | status={t.status} | prioridade={t.priority} | assunto={t.subject}"
            for t in tickets
        ) or "- sem tickets relacionados"
        logs_part = "\n".join(
            f"- {l.timestamp} | {l.service} | {l.level} | {l.message[:200]}"
            for l in logs
        ) or "- sem logs relevantes"

        return (
            "DOCUMENTOS:\n"
            f"{docs_part}\n\n"
            "TICKETS:\n"
            f"{tickets_part}\n\n"
            "LOGS:\n"
            f"{logs_part}"
        )

    @staticmethod
    def _build_prompt(question: str, context: str) -> str:
        return f"""
Você é um analista de suporte técnico sênior.
Use APENAS o contexto fornecido.
Se faltar evidência, diga explicitamente.

Retorne no formato:
DIAGNOSTICO:
<texto curto>
EVIDENCIAS:
- ...
- ...
PROXIMOS_PASSOS:
- ...
- ...

PERGUNTA:
{question}

CONTEXTO:
{context}
"""

    @staticmethod
    def _parse_answer(raw: str) -> CopilotAnswer:
        diagnosis = "Diagnóstico não identificado"
        evidence: List[str] = []
        next_steps: List[str] = []

        section = None
        for line in raw.splitlines():
            clean = line.strip()
            upper = clean.upper()
            if upper.startswith("DIAGNOSTICO"):
                section = "diagnosis"
                continue
            if upper.startswith("EVIDENCIAS"):
                section = "evidence"
                continue
            if upper.startswith("PROXIMOS_PASSOS"):
                section = "steps"
                continue

            if section == "diagnosis" and clean:
                diagnosis = clean.lstrip("- ").strip()
            elif section == "evidence" and clean.startswith("-"):
                evidence.append(clean.lstrip("- ").strip())
            elif section == "steps" and clean.startswith("-"):
                next_steps.append(clean.lstrip("- ").strip())

        return CopilotAnswer(
            diagnosis=diagnosis,
            evidence=evidence or ["Sem evidências suficientes."],
            next_steps=next_steps or ["Coletar mais dados."],
            raw_response=raw,
        )
