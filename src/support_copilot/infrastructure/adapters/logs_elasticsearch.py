from typing import List
from elasticsearch import Elasticsearch
from support_copilot.domain.entities import LogEvent
from support_copilot.infrastructure.config.settings import settings


class ElasticsearchLogProvider:
    def __init__(self) -> None:
        kwargs = {}
        if settings.elasticsearch_api_key:
            kwargs["api_key"] = settings.elasticsearch_api_key
        elif settings.elasticsearch_username and settings.elasticsearch_password:
            kwargs["basic_auth"] = (settings.elasticsearch_username, settings.elasticsearch_password)
        self.client = Elasticsearch(settings.elasticsearch_url, **kwargs)

    def search(self, query: str, limit: int = 10) -> List[LogEvent]:
        body = {
            "size": limit,
            "sort": [{"@timestamp": {"order": "desc"}}],
            "query": {
                "bool": {
                    "should": [
                        {"match": {"message": query}},
                        {"match": {"service": query}},
                    ],
                    "minimum_should_match": 1,
                }
            },
        }
        resp = self.client.search(index=settings.elasticsearch_index, body=body)
        hits = resp.get("hits", {}).get("hits", [])
        events = []
        for hit in hits:
            src = hit.get("_source", {})
            events.append(
                LogEvent(
                    timestamp=str(src.get("@timestamp", "")),
                    service=str(src.get("service", "unknown")),
                    level=str(src.get("level", "INFO")),
                    message=str(src.get("message", "")),
                )
            )
        return events
