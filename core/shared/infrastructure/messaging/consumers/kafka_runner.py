import json
import logging
import time
from kafka import KafkaConsumer

from core.shared.observability.metrics.metrics import (
    EVENTS_PROCESSED,
    EVENT_FAILURES,
    EVENT_PROCESSING_TIME,
)

logger = logging.getLogger(__name__)


class KafkaConsumerRunner:
    def __init__(
        self,
        *,
        topic: str,
        consumer_group: str,
        safe_consumer,
    ):
        self.topic = topic
        self.safe_consumer = safe_consumer

        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers="kafka:9092",
            group_id=consumer_group,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=lambda v: json.loads(v.decode()),
        )

    def run(self):
        logger.info(f"[KAFKA RUNNER STARTED] topic={self.topic}")

        for record in self.consumer:
            start = time.time()
            message = record.value
            event_type = message.get("event_type", "unknown")

            try:
                self.safe_consumer.process(message)

                EVENTS_PROCESSED.labels(
                    consumer=self.safe_consumer.__class__.__name__,
                    event_type=event_type,
                ).inc()

                self.consumer.commit()

            except Exception:
                EVENT_FAILURES.labels(
                    consumer=self.safe_consumer.__class__.__name__,
                    event_type=event_type,
                ).inc()
                raise  # crash hard → Kubernetes/Docker restarts

            finally:
                EVENT_PROCESSING_TIME.labels(
                    consumer=self.safe_consumer.__class__.__name__,
                ).observe(time.time() - start)
