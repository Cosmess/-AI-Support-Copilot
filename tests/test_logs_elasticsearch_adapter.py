from unittest.mock import Mock, patch
from support_copilot.infrastructure.adapters.logs_elasticsearch import ElasticsearchLogProvider


@patch("support_copilot.infrastructure.adapters.logs_elasticsearch.settings")
@patch("support_copilot.infrastructure.adapters.logs_elasticsearch.Elasticsearch")
def test_elasticsearch_adapter_maps_hits(mock_es_cls: Mock, mock_settings: Mock):
    mock_settings.elasticsearch_api_key = ""
    mock_settings.elasticsearch_username = ""
    mock_settings.elasticsearch_password = ""
    mock_settings.elasticsearch_url = "http://localhost:9200"
    mock_settings.elasticsearch_index = "support-logs"

    mock_es = Mock()
    mock_es.search.return_value = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "@timestamp": "2026-05-29T15:00:00Z",
                        "service": "payment-gateway",
                        "level": "WARN",
                        "message": "p95 latency high",
                    }
                }
            ]
        }
    }
    mock_es_cls.return_value = mock_es

    provider = ElasticsearchLogProvider()
    events = provider.search("latency", limit=1)

    assert len(events) == 1
    assert events[0].service == "payment-gateway"
    assert events[0].level == "WARN"
