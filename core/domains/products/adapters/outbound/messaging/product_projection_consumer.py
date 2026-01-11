# filename : core/domains/products/adapters/outbound/messaging/product_projection_consumer.py
import logging

from core.shared.infrastructure.messaging.kafka_consumer import create_consumer
from core.domains.products.read_model.projections.product_event_projection import (
    ProductEventProjection,
)
from core.shared.infrastructure.search.elasticsearch_client import get_es_client


def run_live_product_projection_consumer():
    logging.info(
        "Starting live product projection consumer..., filename : core/domains/products/adapters/outbound/messaging/product_projection_consumer.py"
    )

    consumer = create_consumer(
        topics=["product.events"],
        group_id="product-search-consumer",
        offset_reset="latest",
    )

    es = get_es_client()
    projection = ProductEventProjection(es)

    for message in consumer:
        projection.handle(
            payload=message.value["payload"],
            metadata=message.value["metadata"],
            index_alias="product_search_current",
        )
        consumer.commit()
