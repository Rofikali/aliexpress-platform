# filename: core/shared/infrastructure/messaging/outbox_processor.py

from django.db import transaction
from django.utils import timezone
import logging

from core.shared.models.outbox_event import OutboxEvent
from core.shared.infrastructure.messaging.event_envelope import build_event_envelope

logger = logging.getLogger(__name__)


class OutboxProcessor:
    MAX_RETRIES = 5

    def __init__(self, producer):
        self.producer = producer

    def process_batch(self, batch_size: int = 50):
        with transaction.atomic():
            events = list(
                OutboxEvent.objects.select_for_update(skip_locked=True)
                .filter(status="PENDING", retry_count__lt=self.MAX_RETRIES)
                .order_by("created_at")[:batch_size]
            )

        for event in events:
            self._publish_event(event)

    def _publish_event(self, event: OutboxEvent):
        try:
            envelope = build_event_envelope(event)

            self.producer.send(
                topic=envelope["event_type"],  # product.created
                value=envelope,
            )
            print("Debugging: Sending event to topic:", envelope["event_type"])  # Debugging purposes
            self.producer.flush()

            # 🔐 atomic status update
            with transaction.atomic():
                updated = OutboxEvent.objects.filter(
                    id=event.id, status="PENDING"
                ).update(
                    status="PUBLISHED",
                    published_at=timezone.now(),
                )

                if updated == 0:
                    logger.warning(
                        "Outbox event already processed: %s",
                        event.id,
                    )

        except Exception as e:
            with transaction.atomic():
                event.retry_count += 1
                if event.retry_count >= self.MAX_RETRIES:
                    event.status = "FAILED"

                event.save(update_fields=["retry_count", "status"])

            logger.exception(
                "Failed to publish outbox event %s",
                event.id,
                exc_info=e,
            )


# from django.db import transaction
# from django.utils import timezone
# from core.shared.infrastructure.messaging.event_envelope import build_event_envelope
# from core.shared.models.outbox_event import OutboxEvent
# import logging

# logger = logging.getLogger(__name__)

# TOPIC = "product.events"


# class OutboxProcessor:
#     MAX_RETRIES = 5

#     def __init__(self, producer):
#         self.producer = producer

#     def process_batch(self, batch_size=50):
#         with transaction.atomic():
#             events = list(
#                 OutboxEvent.objects.select_for_update(skip_locked=True)
#                 .filter(status="PENDING", retry_count__lt=self.MAX_RETRIES)
#                 .order_by("created_at")[:batch_size]
#             )

#         for event in events:
#             self._publish(event)

#     def _publish(self, event):
#         try:
#             envelope = build_event_envelope(event)

#             self.producer.send(
#                 topic=TOPIC,
#                 value=envelope,
#             )
#             print("Debuging : Sending event to topic: ", TOPIC)  # Debugging purposes
#             self.producer.flush()

#             with transaction.atomic():
#                 OutboxEvent.objects.filter(id=event.id, status="PENDING").update(
#                     status="PUBLISHED",
#                     published_at=timezone.now(),
#                 )

#         except Exception:
#             with transaction.atomic():
#                 event.retry_count += 1
#                 if event.retry_count >= self.MAX_RETRIES:
#                     event.status = "FAILED"
#                 event.save(update_fields=["retry_count", "status"])

#             logger.exception("Outbox publish failed", extra={"event_id": event.id})
