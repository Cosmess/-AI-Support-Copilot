# 03. Clean Architecture Mapping

## Estrutura implementada

```text
src/support_copilot/
  domain/
  application/
  infrastructure/
  presentation/
```

## Responsabilidades

- `domain`: entidades e contratos (ports), sem dependência externa.
- `application`: casos de uso com regras de orquestração.
- `infrastructure`: adapters para OpenAI, Chroma, Zendesk, Elasticsearch.
- `presentation`: FastAPI e contrato HTTP.

## Dependências permitidas

`presentation -> application -> domain`  
`infrastructure -> domain`  
`application` depende de interfaces do `domain` e não de detalhes externos.
