from typing import Optional


TICKETS_DB = {
    "INC-1001": "Erro de autenticação após rotação de segredo OAuth.",
    "INC-1002": "Timeout intermitente na API de pagamentos entre 10h e 11h.",
    "INC-1003": "Webhook não processado por fila com consumidor parado.",
}

LOGS_DB = {
    "payment timeout": "Logs mostram p95 acima de 9s no serviço payment-gateway.",
    "oauth": "Falha de validação de token: issuer inválido em 23 requisições.",
    "webhook": "Fila support.webhook com backlog de 1.248 mensagens.",
}


def find_ticket(ticket_id: str) -> str:
    return TICKETS_DB.get(ticket_id, "Ticket não encontrado.")


def search_logs(keyword: str) -> str:
    key = keyword.lower().strip()
    return LOGS_DB.get(key, "Nenhum log relevante encontrado para o termo.")


def suggest_priority(impact: Optional[str] = None) -> str:
    mapping = {
        "baixo": "P3 - tratar em janela normal",
        "medio": "P2 - acompanhar hoje",
        "alto": "P1 - tratar imediatamente",
    }
    return mapping.get((impact or "").lower(), "P2 - acompanhar hoje")
