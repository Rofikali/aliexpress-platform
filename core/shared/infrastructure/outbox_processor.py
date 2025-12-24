# from core.shared.infrastructure.message_broker import get_kafka_producer
# from core.shared.models.outbox_event import OutboxEvent


# class OutboxProcessor:
#     BATCH_SIZE = 100

#     def process_batch(self):
#         producer = get_kafka_producer()

#         events = (
#             OutboxEvent.objects.select_for_update(skip_locked=True)
#             .filter(status="PENDING")
#             .order_by("created_at")[: self.BATCH_SIZE]
#         )

#         for event in events:
#             producer.send(
#                 topic=event.event_type,
#                 value={
#                     "id": str(event.id),
#                     "aggregate_id": str(event.aggregate_id),
#                     "type": event.event_type,
#                     "payload": event.payload,
#                 },
#             )

#             event.status = "PUBLISHED"
#             event.save(update_fields=["status"])

from django.db import transaction
from core.shared.models.outbox_event import OutboxEvent


class OutboxProcessor:
    def __init__(self, producer):
        self.producer = producer

    def process_batch(self, batch_size: int = 50):
        events = (
            OutboxEvent.objects
            .select_for_update(skip_locked=True)
            .filter(status="PENDING")
            .order_by("created_at")[:batch_size]
        )

        for event in events:
            self._publish_event(event)

    @transaction.atomic
    def _publish_event(self, event: OutboxEvent):
        try:
            self.producer.send(
                topic=event.event_type,
                value=event.payload,
            )
            event.status = "PUBLISHED"
            event.save(update_fields=["status"])
        except Exception:
            event.status = "FAILED"
            event.save(update_fields=["status"])
            raise
