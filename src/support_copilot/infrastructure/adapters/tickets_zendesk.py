from typing import List
import requests
from support_copilot.domain.entities import TicketEvent
from support_copilot.infrastructure.config.settings import settings


class ZendeskTicketProvider:
    def __init__(self) -> None:
        self.enabled = all([settings.zendesk_subdomain, settings.zendesk_email, settings.zendesk_api_token])
        self.base_url = f"https://{settings.zendesk_subdomain}.zendesk.com/api/v2"
        self.auth = f"{settings.zendesk_email}/token", settings.zendesk_api_token

    def find_by_query(self, query: str, limit: int = 3) -> List[TicketEvent]:
        if not self.enabled:
            return []
        url = f"{self.base_url}/search.json"
        params = {"query": f"type:ticket {query}"}
        resp = requests.get(url, params=params, auth=self.auth, timeout=20)
        resp.raise_for_status()
        payload = resp.json()
        items = payload.get("results", [])[:limit]
        result: List[TicketEvent] = []
        for t in items:
            result.append(
                TicketEvent(
                    ticket_id=str(t.get("id", "")),
                    status=t.get("status", "unknown"),
                    priority=t.get("priority", "normal") or "normal",
                    subject=t.get("subject", ""),
                    description=t.get("description", "")[:1500],
                    tags=t.get("tags", []),
                )
            )
        return result
