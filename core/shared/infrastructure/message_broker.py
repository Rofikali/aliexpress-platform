from kafka import KafkaProducer
import json
from django.conf import settings

_producer = None


def get_kafka_producer():
    global _producer

    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
        )

    return _producer
