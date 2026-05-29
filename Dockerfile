FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY knowledge_base ./knowledge_base
COPY evaluation ./evaluation

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "support_copilot.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
