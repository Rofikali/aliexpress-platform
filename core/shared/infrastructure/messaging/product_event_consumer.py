from core.shared.infrastructure.messaging.consumers.base_consumer import BaseConsumer
from core.shared.infrastructure.messaging.consumers.errors import RetryableError
# from core.shared.infrastructure.database import save_product, DatabaseTimeout


class ProductCreatedConsumer(BaseConsumer):
    def process(self, payload):
        try:
            # DB write
            save_product(payload)
        except DatabaseTimeout:
            raise RetryableError("DB timeout")
