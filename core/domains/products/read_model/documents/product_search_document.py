# # # core/domains/products/read_model/documents/product_search_document.py
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass(frozen=True)
class ProductSearchDocument:
    logging.debug(
        "Product Search Document : "
        "core/domains/products/read_model/documents/product_search_document.py"
    )

    # id: str
    # title: str
    # price: float
    # occurred_at: datetime

    id: str
    title: str
    seller_id: str
    price: float
    status: str
    occurred_at: datetime

    @classmethod
    def from_event(cls, payload: dict, metadata: dict):
        return cls(
            id=metadata["aggregate_id"],  # ✅ ONLY SOURCE OF ID
            title=payload["title"],
            seller_id=payload["seller_id"],
            price=payload["price"],
            status=payload["status"],
            occurred_at=datetime.fromisoformat(metadata["occurred_at"]),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "seller_id": self.seller_id,
            "price": self.price,
            "status": self.status,
            "occurred_at": self.occurred_at.isoformat(),
        }

# from dataclasses import dataclass
# from datetime import datetime


# @dataclass(frozen=True)
# class ProductSearchDocument:
#     id: str
#     title: str
#     seller_id: str
#     status: str
#     occurred_at: datetime
