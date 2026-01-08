from core.shared.infrastructure.messaging.consumers.safe_consumer import SafeConsumer
import logging


class ProductCreatedConsumer(SafeConsumer):
    logging.debug(
        "Initializing ProductCreatedConsumer for topic product.events "
        "and filename : core/shared/infrastructure/messaging/product_event_consumer.py"
    )

    def __init__(self):
        super().__init__(topic="product.events")

    def handle(self, message: dict):
        event_type = message["event_type"]

        if event_type != "product.created":
            return  # ignore unrelated events

        payload = message["payload"]

        # === REAL BUSINESS ACTION ===
        product_id = payload["product_id"]
        print(f"[PRODUCT CREATED] Indexing product {product_id}")

        # Example failure to test retry/DLQ
        if payload.get("force_fail"):
            raise RuntimeError("Simulated processing failure")
