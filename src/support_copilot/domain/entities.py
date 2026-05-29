from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RetrievedDocument:
    source: str
    content: str


@dataclass(frozen=True)
class TicketEvent:
    ticket_id: str
    status: str
    priority: str
    subject: str
    description: str
    tags: List[str]


@dataclass(frozen=True)
class LogEvent:
    timestamp: str
    service: str
    level: str
    message: str


@dataclass(frozen=True)
class CopilotAnswer:
    diagnosis: str
    evidence: List[str]
    next_steps: List[str]
    raw_response: str
