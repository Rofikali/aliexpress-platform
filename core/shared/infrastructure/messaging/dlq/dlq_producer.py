# # # filename : core/shared/infrastructure/messaging/dlq/dlq_producer.py
# # import json
# # import os
# # from kafka import KafkaProducer

# # DLQ_TOPIC_PREFIX = os.getenv("DLQ_TOPIC_PREFIX", "dlq.")
# # GROUP_ID = "product-dlq-consumer-group"


# # class DLQProducer:
# #     def __init__(self, bootstrap_servers):
# #         self.producer = KafkaProducer(
# #             bootstrap_servers=bootstrap_servers,
# #             value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# #         )

# #     def send_to_dlq(self, original_topic, envelope, reason):
# #         dlq_topic = f"{DLQ_TOPIC_PREFIX}{original_topic}"

# #         message = {
# #             "original_topic": original_topic,
# #             "event_id": envelope.get("event_id"),
# #             "event_type": envelope.get("event_type"),
# #             "version": envelope.get("version"),
# #             "occurred_at": envelope.get("occurred_at"),
# #             "payload": envelope.get("payload"),
# #             "reason": reason,
# #         }

# #         self.producer.send(dlq_topic, message)
# #         self.producer.flush()


# # filename : core/shared/infrastructure/messaging/dlq/dlq_producer.py
# from datetime import datetime
# from core.shared.infrastructure.messaging.broker.kafka_producer import (
#     get_kafka_producer,
# )


# class DLQProducer:
#     def __init__(self):
#         self.producer = get_kafka_producer()

#     def send_to_dlq(self, *, original_topic: str, envelope: dict, reason: str):
#         dlq_event = {
#             "event_id": envelope["event_id"],
#             "event_type": envelope["event_type"],
#             "original_topic": original_topic,
#             "failed_at": datetime.utcnow().isoformat(),
#             "reason": reason,
#             "payload": envelope,
#         }

#         self.producer.send(
#             f"{original_topic}.dlq",
#             key=envelope["event_id"],
#             value=dlq_event,
#         )

# filename : core/shared/infrastructure/messaging/dlq/dlq_producer.py
# import logging
# from datetime import datetime
# from core.shared.infrastructure.messaging.message_broker import publish_event
# from core.shared.infrastructure.messaging.broker.kafka_producer import (
#     get_kafka_producer,
# )

# logger = logging.getLogger(__name__)


# class DLQProducer:
#     DLQ_TOPIC = "dlq.product.events"

#     def send_to_dlq(
#         self,
#         original_topic: str,
#         message: dict,
#         *,
#         reason: str,
#     ) -> None:
#         dlq_event = {
#             "original_topic": original_topic,
#             "failed_at": datetime.utcnow().isoformat(),
#             "reason": reason,
#             "payload": message,
#         }

#         publish_event(self.DLQ_TOPIC, dlq_event)

#         logger.error(
#             "Event sent to DLQ",
#             extra={
#                 "original_topic": original_topic,
#                 "reason": reason,
#             },
#         )


import logging
from datetime import datetime
from core.shared.infrastructure.messaging.broker import get_kafka_producer

logger = logging.getLogger(__name__)


class DLQProducer:
    DLQ_TOPIC = "dlq.product.events"

    def __init__(self):
        self.producer = get_kafka_producer()

    def send_to_dlq(
        self,
        original_topic: str,
        message: dict,
        *,
        reason: str,
    ) -> None:
        dlq_event = {
            "original_topic": original_topic,
            "failed_at": datetime.now().isoformat(),
            "reason": reason,
            "payload": message,
        }

        self.producer.send(
            topic=self.DLQ_TOPIC,
            key=original_topic,
            value=dlq_event,
        )

        logger.error(
            "Event sent to DLQ",
            extra={
                "original_topic": original_topic,
                "reason": reason,
            },
        )
