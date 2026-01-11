# filename: core/domains/products/adapters/inbound/consumer/product_event_consumer.py
import logging
from core.shared.infrastructure.messaging.kafka_consumer import create_consumer
from core.shared.infrastructure.safe_consumer import safe_handle_event
from core.domains.products.read_model.projections.product_event_projection import (
    ProductEventProjection,
)
from core.shared.infrastructure.messaging.consumers.errors import BusinessError
from core.shared.infrastructure.search.elasticsearch_client import get_es_client

TOPICS = ["product.events"]
GROUP_ID = "product-event-projection-group"

projection = ProductEventProjection(get_es_client())


def handle_product_event(event: dict):
    event_type = event["event_type"]
    payload = event["payload"]
    metadata = event["metadata"]

    if event_type in ("product.created", "product.updated"):
        projection.index(payload, metadata)
    elif event_type == "product.deleted":
        projection.delete(payload)
    else:
        raise BusinessError(f"Unsupported event type: {event_type}")


def run_product_event_consumer(override_index: str | None = None, once: bool = False):
    if override_index:
        logging.debug(
            f"Overriding index to {override_index} "
            "in core/domains/products/adapters/inbound/consumer/product_event_consumer.py"
        )
        projection.INDEX = override_index

    if once:
        logging.debug(
            "Running consumer in once mode "
            "in core/domains/products/adapters/inbound/consumer/product_event_consumer.py"
        )
        consumer = create_consumer(TOPICS, GROUP_ID)

        message = next(consumer)
        safe_handle_event(
            consumer=consumer,
            message=message,
            handler_fn=handle_product_event,
            consumer_name=GROUP_ID,
        )
    else:
        logging.debug(
            "Running consumer in continuous mode "
            "in core/domains/products/adapters/inbound/consumer/product_event_consumer.py"
        )
