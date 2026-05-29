from datetime import datetime, timezone
from elasticsearch import Elasticsearch, helpers


def main() -> None:
    client = Elasticsearch("http://localhost:9200")
    index = "support-logs"
    docs = [
        {
            "_index": index,
            "_source": {
                "@timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "webhook-worker",
                "level": "ERROR",
                "message": "Webhook processing timeout after 30s. Backlog increasing.",
            },
        },
        {
            "_index": index,
            "_source": {
                "@timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "payment-gateway",
                "level": "WARN",
                "message": "p95 latency reached 9.2 seconds for authorize endpoint.",
            },
        },
        {
            "_index": index,
            "_source": {
                "@timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "auth-service",
                "level": "ERROR",
                "message": "OAuth token validation failed: issuer mismatch.",
            },
        },
    ]
    helpers.bulk(client, docs)
    client.indices.refresh(index=index)
    print("Seeded support logs in Elasticsearch index:", index)


if __name__ == "__main__":
    main()
