from django.core.management.base import BaseCommand
from time import sleep

from core.shared.infrastructure.outbox_processor import OutboxProcessor
from core.domains.products.outbox.product_outbox_model import ProductOutbox
from core.domains.products.adapters.outbound.messaging.topic_resolver import (
    product_topic_resolver,
)


class Command(BaseCommand):
    help = "Process outbox events and publish to Kafka"

    def handle(self, *args, **options):
        processor = OutboxProcessor(
            model=ProductOutbox,
            topic_resolver=product_topic_resolver,
        )

        self.stdout.write("Outbox processor started")

        while True:
            processor.process_batch()
            sleep(1)
