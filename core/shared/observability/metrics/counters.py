from prometheus_client import Counter

# Total number of messages pushed to DLQ
DLQ_COUNTER = Counter(
    "consumer_dlq_total", "Total number of messages sent to DLQ", ["topic", "reason"]
)

# Total number of retry attempts
RETRY_COUNTER = Counter(
    "consumer_retry_total", "Total number of retries attempted per topic", ["topic"]
)
