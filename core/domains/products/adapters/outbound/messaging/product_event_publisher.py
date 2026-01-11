# # core/domains/products/adapters/outbound/messaging/product_event_publisher.py

from core.domains.products.outbox.product_outbox_model import ProductOutbox


class ProductEventPublisher:
    def publish_all(self, events):
        for event in events:
            ProductOutbox.objects.create(
                aggregate_id=event.aggregate_id,  # ✅ FIX
                event_type=event.event_type,
                payload=event.to_primitives(),
                status="PENDING",
            )
