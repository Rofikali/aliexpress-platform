# # filename : core/shared/infrastructure/safe_consumer.py
# import logging
# import time
# from core.shared.infrastructure.messaging.consumers.retry_policy import (
#     should_retry,
#     increment_retry,
# )
# from core.shared.infrastructure.messaging.publisher import (
#     publish_retry,
#     publish_to_dlq,
# )
# from core.shared.observability.metrics.metrics import (
#     EVENTS_PROCESSED,
#     EVENT_PROCESSING_TIME,
#     EVENT_FAILURES,
# )


# def safe_handle_event(
#     *,
#     event: dict,
#     topic: str,
#     handler_fn,
#     consumer_name: str,
# ):
#     start = time.time()

#     try:
#         handler_fn(event)

#         EVENTS_PROCESSED.labels(
#             consumer=consumer_name,
#             event_type=event["event_type"],
#         ).inc()

#     except Exception as exc:
#         EVENT_FAILURES.labels(
#             consumer=consumer_name,
#             event_type=event["event_type"],
#         ).inc()

#         if should_retry(event):
#             logging.debug(
#                 f"Sending event to DLQ for topic {topic} due to reason: {str(exc)}, "
#                 f"and filename : core/shared/infrastructure/safe_consumer.py"
#             )
#             retry_event = increment_retry(event)
#             publish_retry(topic, retry_event)
#         else:
#             publish_to_dlq(topic, event, str(exc))

#     finally:
#         EVENT_PROCESSING_TIME.labels(
#             consumer=consumer_name,
#         ).observe(time.time() - start)

# filename : core/shared/infrastructure/safe_consumer.py

import time
from core.shared.infrastructure.messaging.publisher import (
    publish_retry,
    publish_to_dlq,
)
from core.shared.infrastructure.messaging.consumers.retry_policy import should_retry
from core.shared.infrastructure.messaging.envelope.event_envelope import EventEnvelope
from core.shared.infrastructure.messaging.consumers.errors import (
    BusinessError,
    RetryableBusinessError,
    InfrastructureError,
)
from core.shared.observability.metrics.metrics import (
    EVENTS_PROCESSED,
    EVENT_PROCESSING_TIME,
    EVENT_FAILURES,
)


def safe_handle_event(
    *,
    consumer,
    message,
    handler_fn,
    consumer_name: str,
):
    start = time.time()
    event = message.value
    topic = message.topic

    try:
        handler_fn(event)

        EVENTS_PROCESSED.labels(
            consumer=consumer_name,
            event_type=event["event_type"],
        ).inc()

        consumer.commit()

    except RetryableBusinessError as exc:
        EVENT_FAILURES.labels(
            consumer=consumer_name,
            event_type=event["event_type"],
        ).inc()

        if should_retry(event):
            retry_event = EventEnvelope.increment_retry(event)
            publish_retry(f"{topic}.retry", retry_event)
            consumer.commit()
        else:
            publish_to_dlq(topic, event, str(exc))
            consumer.commit()

    except BusinessError as exc:
        EVENT_FAILURES.labels(
            consumer=consumer_name,
            event_type=event["event_type"],
        ).inc()

        publish_to_dlq(topic, event, str(exc))
        consumer.commit()

    except InfrastructureError:
        # DO NOT COMMIT — crash the consumer
        raise

    finally:
        EVENT_PROCESSING_TIME.labels(
            consumer=consumer_name,
        ).observe(time.time() - start)
