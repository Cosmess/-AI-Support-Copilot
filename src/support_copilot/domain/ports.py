from typing import Protocol, List
from support_copilot.domain.entities import RetrievedDocument, TicketEvent, LogEvent


class KnowledgeRepository(Protocol):
    def retrieve(self, question: str, k: int = 4) -> List[RetrievedDocument]:
        ...


class TicketProvider(Protocol):
    def find_by_query(self, query: str, limit: int = 3) -> List[TicketEvent]:
        ...


class LogProvider(Protocol):
    def search(self, query: str, limit: int = 10) -> List[LogEvent]:
        ...


class LLMProvider(Protocol):
    def answer(self, prompt: str) -> str:
        ...
