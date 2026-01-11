# filename : core/domains/products/read_model/rebuild/rebuild_product_read_model.py

import logging

from core.shared.infrastructure.messaging.kafka_consumer import create_replay_consumer
from core.domains.products.read_model.projections.product_event_projection import (
    ProductEventProjection,
)
from core.shared.infrastructure.search.elasticsearch_client import get_es_client


def replay_product_events(index_name: str):
    logging.info(
        "Starting replay of product events to rebuild read model..., filename : core/domains/products/read_model/rebuild/rebuild_product_read_model.py"
    )

    consumer = create_replay_consumer(
        topics=["product.events"],
    )

    es = get_es_client()
    projection = ProductEventProjection(es)

    consumer.poll(timeout_ms=0)
    consumer.seek_to_beginning()

    processed = 0

    while True:
        records = consumer.poll(timeout_ms=1000)
        if not records:
            break  # 🔥 FINITE EXIT

        for batch in records.values():
            for record in batch:
                projection.handle(
                    payload=record.value["payload"],
                    metadata=record.value["metadata"],
                    index_name=index_name,
                )
                processed += 1

    consumer.close()
    return processed
