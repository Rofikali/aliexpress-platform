# filename : core/shared/adapters/inbound/consumer/dlq_consumer.py
from core.shared.read_model.models.dlq_event import DeadLetterEvent
import logging


def handle_dlq_event(event):
    logging.debug(
        f"Handling DLQ event for topic {event.get('topic')} and aggregate_id {event['aggregate_id']}"
        f"and filename : core/shared/adapters/inbound/consumer/dlq_consumer.py"
    )
    DeadLetterEvent.objects.create(
        id=event["aggregate_id"],
        topic=event.get("topic"),
        event_type=event["type"],
        payload=event["payload"],
        retry_count=event["retry_count"],
        reason=event["dlq_reason"],
    )
