# from core.shared.infrastructure.messaging.consumers.schema_compatibility import (
#     check_compatibility,
#     IncompatibleSchemaError,
# )


# class BaseConsumer:
#     def handle_message(self, envelope: dict):
#         event_type = envelope["event_type"]
#         version = envelope["version"]
#         payload = envelope["payload"]

#         try:
#             check_compatibility(event_type, version, payload)
#         except IncompatibleSchemaError as e:
#             self.on_schema_error(envelope, e)
#             return

#         self.process(payload)

#     def process(self, payload: dict):
#         raise NotImplementedError

#     def on_schema_error(self, envelope: dict, error: Exception):
#         # DLQ comes later — for now we log loudly
#         print(f"[SCHEMA ERROR] {error}")


# filename : core/shared/infrastructure/messaging/consumers/base_consumer.py


from core.shared.infrastructure.messaging.consumers.retry_policy import RetryPolicy
from core.shared.infrastructure.messaging.consumers.retry_executor import RetryExecutor
from core.shared.infrastructure.messaging.consumers.errors import (
    RetryableError,
    NonRetryableError,
)
from core.shared.infrastructure.observability.metrics.consumer_metrics import (
    ConsumerMetrics,
)
from core.shared.infrastructure.messaging.consumers.schema_compatibility import (
    check_compatibility,
    IncompatibleSchemaError,
)

from core.shared.infrastructure.messaging.dlq.dlq_producer import DLQProducer
import os

DLQ_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


class BaseConsumer:
    retry_policy = RetryPolicy()
    dlq_producer = DLQProducer(DLQ_BOOTSTRAP_SERVERS)

    def handle_message(self, envelope: dict):
        event_type = envelope["event_type"]
        version = envelope["version"]
        payload = envelope["payload"]

        # 1️⃣ Schema compatibility
        try:
            check_compatibility(event_type, version, payload)
        except IncompatibleSchemaError as e:
            self.on_schema_error(envelope, e)
            return

        # 2️⃣ Retryable execution
        executor = RetryExecutor(self.retry_policy)

        try:
            executor.execute(lambda: self.process(payload))
        except RetryableError as e:
            self.on_retry_exhausted(envelope, e)
        except NonRetryableError as e:
            self.on_non_retryable_error(envelope, e)

    def process(self, payload: dict):
        raise NotImplementedError

    # def on_schema_error(self, envelope, error):
    #     print(f"[SCHEMA ERROR] {error}")
    #     self.dlq_producer.send_to_dlq(
    #         envelope.get("topic", "unknown"), envelope, reason=f"Schema Error: {error}"
    #     )

    # def on_retry_exhausted(self, envelope, error):
    #     print(f"[RETRY EXHAUSTED] {error}")
    #     self.dlq_producer.send_to_dlq(
    #         envelope.get("topic", "unknown"),
    #         envelope,
    #         reason=f"Retry Exhausted: {error}",
    #     )

    # def on_non_retryable_error(self, envelope, error):
    #     print(f"[NON-RETRYABLE] {error}")
    #     self.dlq_producer.send_to_dlq(
    #         envelope.get("topic", "unknown"), envelope, reason=f"Non-Retryable: {error}"
    #     )


# class BaseConsumer:
#     ...

    def on_schema_error(self, envelope, error):
        print(f"[SCHEMA ERROR] {error}")
        self.dlq_producer.send_to_dlq(
            envelope.get("topic", "unknown"), envelope, reason=f"Schema Error: {error}"
        )
        ConsumerMetrics.increment_dlq(
            envelope.get("topic", "unknown"), reason="Schema Error"
        )

    def on_retry_exhausted(self, envelope, error):
        print(f"[RETRY EXHAUSTED] {error}")
        self.dlq_producer.send_to_dlq(
            envelope.get("topic", "unknown"),
            envelope,
            reason=f"Retry Exhausted: {error}",
        )
        ConsumerMetrics.increment_dlq(
            envelope.get("topic", "unknown"), reason="Retry Exhausted"
        )

    def on_retry_attempt(self, envelope):
        ConsumerMetrics.increment_retry(envelope.get("topic", "unknown"))

    def on_non_retryable_error(self, envelope, error):
        print(f"[NON-RETRYABLE] {error}")
        self.dlq_producer.send_to_dlq(
            envelope.get("topic", "unknown"), envelope, reason=f"Non-Retryable: {error}"
        )
        ConsumerMetrics.increment_dlq(
            envelope.get("topic", "unknown"), reason="Non-Retryable"
        )






# class BaseConsumer:
#     retry_policy = RetryPolicy()
#     dlq_producer = DLQProducer(DLQ_BOOTSTRAP_SERVERS)

#     def handle_message(self, envelope: dict):
#         event_type = envelope["event_type"]
#         version = envelope["version"]
#         payload = envelope["payload"]

#         # 1️⃣ Schema compatibility
#         try:
#             check_compatibility(event_type, version, payload)
#         except IncompatibleSchemaError as e:
#             self.on_schema_error(envelope, e)
#             return

#         # 2️⃣ Retryable execution
#         executor = RetryExecutor(self.retry_policy)

#         try:
#             executor.execute(lambda: self.process(payload))
#         except RetryableError as e:
#             self.on_retry_exhausted(envelope, e)
#         except NonRetryableError as e:
#             self.on_non_retryable_error(envelope, e)

#     def process(self, payload: dict):
#         raise NotImplementedError

#     def on_schema_error(self, envelope, error):
#         print(f"[SCHEMA ERROR] {error}")

#     def on_retry_exhausted(self, envelope, error):
#         print(f"[RETRY EXHAUSTED] {error}")
#         # DLQ comes next step

#     def on_non_retryable_error(self, envelope, error):
#         print(f"[NON-RETRYABLE] {error}")
