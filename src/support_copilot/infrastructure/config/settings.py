import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    app_name: str = "AI Support Copilot"
    environment: str = os.getenv("ENVIRONMENT", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    api_auth_token: str = os.getenv("API_AUTH_TOKEN", "")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_embeddings_model: str = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")

    vector_store_dir: str = os.getenv("VECTOR_STORE_DIR", "./data/chroma")
    knowledge_base_dir: str = os.getenv("KNOWLEDGE_BASE_DIR", "./knowledge_base")

    zendesk_subdomain: str = os.getenv("ZENDESK_SUBDOMAIN", "")
    zendesk_email: str = os.getenv("ZENDESK_EMAIL", "")
    zendesk_api_token: str = os.getenv("ZENDESK_API_TOKEN", "")

    elasticsearch_url: str = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
    elasticsearch_index: str = os.getenv("ELASTICSEARCH_INDEX", "support-logs")
    elasticsearch_api_key: str = os.getenv("ELASTICSEARCH_API_KEY", "")
    elasticsearch_username: str = os.getenv("ELASTICSEARCH_USERNAME", "")
    elasticsearch_password: str = os.getenv("ELASTICSEARCH_PASSWORD", "")


settings = Settings()
