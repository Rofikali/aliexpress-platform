# filename : core/shared/infrastructure/safe_consumer.py
import logging
import time
from core.shared.infrastructure.messaging.consumers.retry_policy import (
    should_retry,
    increment_retry,
)
from core.shared.infrastructure.messaging.publisher import (
    publish_retry,
    publish_to_dlq,
)
from core.shared.observability.metrics.metrics import (
    EVENTS_PROCESSED,
    EVENT_PROCESSING_TIME,
    EVENT_FAILURES,
)


def safe_handle_event(
    *,
    event: dict,
    topic: str,
    handler_fn,
    consumer_name: str,
):
    start = time.time()

    try:
        handler_fn(event)

        EVENTS_PROCESSED.labels(
            consumer=consumer_name,
            event_type=event["event_type"],
        ).inc()

    except Exception as exc:
        EVENT_FAILURES.labels(
            consumer=consumer_name,
            event_type=event["event_type"],
        ).inc()

        if should_retry(event):
            logging.debug(
                f"Sending event to DLQ for topic {topic} due to reason: {str(exc)}, "
                f"and filename : core/shared/infrastructure/safe_consumer.py"
            )
            retry_event = increment_retry(event)
            publish_retry(topic, retry_event)
        else:
            publish_to_dlq(topic, event, str(exc))

    finally:
        EVENT_PROCESSING_TIME.labels(
            consumer=consumer_name,
        ).observe(time.time() - start)
