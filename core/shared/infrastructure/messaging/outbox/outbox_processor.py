# filename: core/shared/infrastructure/messaging/outbox_processor.py

import logging
from core.shared.infrastructure.messaging.envelope.event_envelope import (
    build_event_envelope,
)

from core.shared.infrastructure.messaging.routing.event_routing import route_event

logger = logging.getLogger(__name__)


class OutboxProcessor:
    def __init__(self, producer):
        self.producer = producer

    def publish(self, event):
        envelope = build_event_envelope(event)
        topic = route_event(event.event_type)

        # future = self.producer.send(
        #     topic=topic,
        #     key=str(event.aggregate_id),
        #     value=envelope,
        # )
        future = self.producer.send(
            topic=topic,
            key=str(event.aggregate_id),
            value=envelope,
        )

        future.get(timeout=10)
        logger.info("Published event %s to %s", event.event_type, topic)
