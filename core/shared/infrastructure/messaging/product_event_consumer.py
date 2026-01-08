from core.shared.infrastructure.messaging.consumers.base_consumer import BaseConsumer
from core.shared.infrastructure.messaging.consumers.errors import RetryableError

# from core.shared.infrastructure.database import save_product, DatabaseTimeout
import logging


class ProductCreatedConsumer(BaseConsumer):
    def process(self, payload):
        try:
            # DB write
            logging.debug(
                f"Processing product.created event for aggregate_id {payload['aggregate_id']} "
                f"and filename : core/shared/infrastructure/messaging/product_event_consumer.py"
            )
            save_product(payload)
        except DatabaseTimeout:
            logging.debug(
                f"Database timeout occurred while processing product.created event for aggregate_id {payload['aggregate_id']} "
                f"and filename : core/shared/infrastructure/messaging/product_event_consumer.py"
            )
            raise RetryableError("DB timeout")
