from unittest.mock import Mock, patch
from support_copilot.infrastructure.adapters.tickets_zendesk import ZendeskTicketProvider


@patch("support_copilot.infrastructure.adapters.tickets_zendesk.settings")
@patch("support_copilot.infrastructure.adapters.tickets_zendesk.requests.get")
def test_zendesk_adapter_maps_response(mock_get: Mock, mock_settings: Mock):
    mock_settings.zendesk_subdomain = "acme"
    mock_settings.zendesk_email = "bot@acme.com"
    mock_settings.zendesk_api_token = "token"

    response = Mock()
    response.json.return_value = {
        "results": [
            {
                "id": 123,
                "status": "open",
                "priority": "high",
                "subject": "Erro no webhook",
                "description": "Backlog aumentando",
                "tags": ["webhook"],
            }
        ]
    }
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    provider = ZendeskTicketProvider()
    items = provider.find_by_query("webhook", limit=1)

    assert len(items) == 1
    assert items[0].ticket_id == "123"
    assert items[0].status == "open"
