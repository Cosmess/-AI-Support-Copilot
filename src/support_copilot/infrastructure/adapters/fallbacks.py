from typing import List
from support_copilot.domain.entities import TicketEvent, LogEvent


class NullTicketProvider:
    def find_by_query(self, query: str, limit: int = 3) -> List[TicketEvent]:
        return []


class NullLogProvider:
    def search(self, query: str, limit: int = 10) -> List[LogEvent]:
        return []
