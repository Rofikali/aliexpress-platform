from django.utils.timezone import now
from core.shared.infrastructure.kafka_producer import publish_event
from core.shared.read_model.models.dlq_event import DeadLetterEvent


class DLQReplayService:
    def replay(self, dlq_event_id):
        dlq_event = DeadLetterEvent.objects.get(id=dlq_event_id)

        if dlq_event.status != "PENDING":
            raise ValueError("Event already replayed")

        publish_event(
            dlq_event.topic,
            {
                **dlq_event.payload,
                "retry_count": 0,
            },
        )

        dlq_event.status = "REPLAYED"
        dlq_event.replayed_at = now()
        dlq_event.save()
