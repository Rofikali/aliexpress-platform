# filename : core/shared/infrastructure/kafka_consumer.py

from kafka import KafkaConsumer
import json
from django.conf import settings


def create_consumer(topics, group_id):
    return KafkaConsumer(
        *topics,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        enable_auto_commit=False,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
    )


# from kafka import KafkaConsumer
# import json


# def build_consumer(topic: str, group_id: str):
#     return KafkaConsumer(
#         topic,
#         bootstrap_servers="kafka:9092",
#         group_id=group_id,
#         auto_offset_reset="earliest",
#         enable_auto_commit=True,
#         value_deserializer=lambda m: json.loads(m.decode("utf-8")),
#     )
