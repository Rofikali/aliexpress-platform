from django.core.management.base import BaseCommand
from core.shared.infrastructure.messaging.kafka_consumer import build_consumer
from core.shared.infrastructure.messaging.consumers.product_consumer import (
    ProductCreatedConsumer,
)


class Command(BaseCommand):
    help = "Run product Kafka consumer"

    def handle(self, *args, **options):
        consumer = build_consumer(
            topic="product.events",
            group_id="product-consumer-group",
        )
        handler = ProductCreatedConsumer()

        self.stdout.write("Product consumer started")

        for msg in consumer:
            handler.process(msg.value)
