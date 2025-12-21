from django.db import transaction
from core.shared.infrastructure.message_broker import get_kafka_producer


class OutboxProcessor:
    """
    Generic processor — works for ALL domains
    """

    def __init__(self, model, topic_resolver):
        self.model = model
        self.topic_resolver = topic_resolver
        self.producer = get_kafka_producer()

    def process_batch(self, batch_size=100):
        with transaction.atomic():
            events = (
                self.model.objects.select_for_update(skip_locked=True)
                .filter(published=False)
                .order_by("created_at")[:batch_size]
            )

            for event in events:
                topic = self.topic_resolver(event)
                self.producer.send(topic, event.payload)

                event.published = True
                event.save(update_fields=["published"])
