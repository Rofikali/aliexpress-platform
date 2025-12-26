from prometheus_client import Counter, Histogram

EVENTS_PROCESSED = Counter(
    "events_processed_total",
    "Total events processed",
    ["consumer", "event_type"],
)

EVENT_PROCESSING_TIME = Histogram(
    "event_processing_seconds",
    "Event processing time",
    ["consumer"],
)

EVENT_FAILURES = Counter(
    "event_failures_total",
    "Total failed events",
    ["consumer", "event_type"],
)
