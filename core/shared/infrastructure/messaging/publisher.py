# filename : core/shared/infrastructure/messaging/publisher.py
from core.shared.infrastructure.messaging.broker.kafka_producer import (
    get_kafka_producer,
)
from core.shared.infrastructure.messaging.dlq.dlq_producer import DLQProducer


_producer = None
_dlq = None


def _get_producer():
    global _producer
    if not _producer:
        _producer = get_kafka_producer()
    return _producer


def _get_dlq():
    global _dlq
    if not _dlq:
        _dlq = DLQProducer(
            bootstrap_servers=_get_producer().config["bootstrap_servers"]
        )
    return _dlq


def publish_retry(topic: str, event: dict):
    aggregate_id = event.get("aggregate_id")
    if not aggregate_id:
        raise ValueError("Event missing aggregate_id")

    producer = _get_producer()
    producer.send(
        topic,
        key=str(aggregate_id),
        value=event,
    )


import logging


def publish_to_dlq(original_topic: str, envelope: dict, reason: str):
    logging.debug(
        f"Sending event to DLQ for topic {original_topic} due to reason: {reason}, "
        f"and filename : core/shared/infrastructure/messaging/publisher.py"
    )

    dlq = _get_dlq()
    dlq.send_to_dlq(original_topic, envelope, reason)
