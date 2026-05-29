# Runbooks técnicos

## Webhook parado

Sintomas:
- backlog crescendo em fila de webhook
- eventos sem processamento

Ações:
1. Verificar consumidor da fila.
2. Reiniciar worker com segurança.
3. Reprocessar mensagens em dead-letter queue, se aplicável.

## Timeout em gateway de pagamento

Sintomas:
- aumento de latência p95/p99
- erros de timeout no cliente

Ações:
1. Validar dependências externas.
2. Habilitar circuit breaker temporário.
3. Reduzir timeout agressivo no cliente interno.
