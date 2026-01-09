# filename: core/domains/products/adapters/inbound/consumer/product_event_consumer.py
import logging
from core.shared.infrastructure.messaging.kafka_consumer import create_consumer
from core.shared.infrastructure.safe_consumer import safe_handle_event
from core.domains.products.read_model.projections.product_event_projection import (
    ProductEventProjection,
)
from core.shared.infrastructure.messaging.consumers.errors import BusinessError

TOPICS = ["product.events"]
GROUP_ID = "product-event-projection-group"

projection = ProductEventProjection()


# def handle_product_event(event: dict):
#     logging.debug(
#         "Handling product event: "
#         "core/domains/products/adapters/inbound/consumer/product_event_consumer.py"
#     )
#     event_type = event["event_type"]

#     if event_type in ("product.created", "product.updated"):
#         projection.index(event["payload"])
#     elif event_type == "product.deleted":
#         projection.delete(event["payload"]["product_id"])
#     else:
#         raise BusinessError(f"Unsupported event type: {event_type}")


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


def run_product_event_consumer():
    logging.debug(
        "Run product event Consumer : "
        "core/domains/products/adapters/inbound/consumer/product_event_consumer.py"
    )
    consumer = create_consumer(TOPICS, GROUP_ID)

    for message in consumer:
        safe_handle_event(
            consumer=consumer,
            message=message,
            handler_fn=handle_product_event,
            consumer_name=GROUP_ID,
        )
