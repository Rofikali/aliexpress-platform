from core.shared.models.outbox_event import OutboxEvent
from django.db import transaction
import uuid


class ProductService:
    @transaction.atomic
    def create_product(self, data: dict):
        product_id = uuid.uuid4()

        # 1️⃣ Save product (omitted here)
        # Product.objects.create(...)

        # 2️⃣ Write outbox event (THIS IS THE PRODUCER)
        OutboxEvent.objects.create(
            aggregate_type="product",
            aggregate_id=product_id,
            event_type="product.created",
            payload={
                "id": str(product_id),
                "seller_id": data["seller_id"],
                "title": data["title"],
                # "price": data["price"],
            },
        )

        return product_id

        # "product_id": str(self.aggregate_id),
        # "seller_id": str(self.seller_id),
        # "title": self.title,
