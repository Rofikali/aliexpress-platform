# # filename : core/shared/infrastructure/messaging/envelope/event_envelope.py
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any


@dataclass(frozen=True)
class EventEnvelope:
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any]
    version: int
    retries: int
    created_at: str


def build_event_envelope(outbox_event) -> dict:
    """
    Builds Kafka envelope from an OutboxEvent (DB model).
    """

    occurred_at = (
        outbox_event.occurred_at
        if hasattr(outbox_event, "occurred_at") and outbox_event.occurred_at
        else outbox_event.created_at
    )

    return EventEnvelope(
        event_id=str(uuid4()),
        event_type=outbox_event.event_type,
        payload=outbox_event.payload,
        metadata={
            "aggregate_id": str(outbox_event.aggregate_id),
            "aggregate_type": outbox_event.aggregate_type,
            "occurred_at": occurred_at.isoformat(),
            "outbox_id": str(outbox_event.id),
        },
        version=outbox_event.event_version,
        retries=outbox_event.retry_count,
        created_at=datetime.utcnow().isoformat(),
    ).__dict__
