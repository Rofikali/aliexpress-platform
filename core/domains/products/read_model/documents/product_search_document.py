# # core/domains/products/read_model/documents/product_search_document.py
# # core/domains/products/read_model/documents/product_search_document.py
# from dataclasses import dataclass
# from typing import Optional
# from datetime import datetime
# import logging


# @dataclass(frozen=True)
# class ProductSearchDocument:
#     id: str
#     title: str
#     price: Optional[float]
#     seller_id: str
#     status: str
#     occurred_at: datetime  # ← important rename

#     @classmethod
#     def from_event(cls, payload: dict, metadata: dict) -> "ProductSearchDocument":
#         logging.debug(
#             f"Creating ProductSearchDocument: id={id}, title={payload}, seller_id={metadata}, status={metadata}, occurred_at={metadata}"
#         )
#         data = payload.get("data")
#         if not data:
#             raise ValueError("Event payload missing 'data'")

#         product_id = data.get("product_id")
#         if not product_id:
#             raise ValueError("product_id is required for search projection")

#         occurred_at = metadata.get("occurred_at")
#         if not occurred_at:
#             raise ValueError("Event metadata missing 'occurred_at'")

#         return cls(
#             id=product_id,
#             title=data["title"],
#             seller_id=data["seller_id"],
#             price=data.get("price"),
#             status=data.get("status", "UNKNOWN"),
#             occurred_at=datetime.fromisoformat(occurred_at),
#         )


# # from dataclasses import dataclass
# # from datetime import datetime


# # @dataclass(frozen=True)
# # class ProductSearchDocument:
# #     id: str
# #     name: str
# #     price: float
# #     created_at: datetime

# #     @classmethod
# #     def from_event(cls, payload: dict, metadata: dict):
# #         return cls(
# #             id=metadata["aggregate_id"],           # ✅ SOURCE OF TRUTH
# #             name=payload["name"],
# #             price=payload["price"],
# #             created_at=datetime.fromisoformat(
# #                 metadata["occurred_at"]
# #             ),
# #         )


# # from dataclasses import dataclass
# # from datetime import datetime


# # @dataclass(frozen=True)
# # class ProductSearchDocument:
# #     id: str
# #     name: str
# #     price: float
# #     created_at: datetime

# #     @classmethod
# #     def from_event(cls, payload: dict, metadata: dict):
# #         return cls(
# #             id=metadata["aggregate_id"],           # ✅ SOURCE OF TRUTH
# #             name=payload["name"],
# #             price=payload["price"],
# #             created_at=datetime.fromisoformat(
# #                 metadata["occurred_at"]
# #             ),
# #         )


from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ProductSearchDocument:
    id: str
    title: str
    seller_id: str
    status: str
    occurred_at: datetime

    @classmethod
    def from_event(cls, payload: dict, metadata: dict) -> "ProductSearchDocument":
        """
        Read-model adapter.
        Translates domain event → search document.
        """

        data = payload.get("data")
        if not data:
            raise ValueError("Event payload missing 'data'")

        product_id = data.get("product_id")
        if not product_id:
            raise ValueError("product_id is required")

        occurred_at = metadata.get("occurred_at")
        if not occurred_at:
            raise ValueError("Event metadata missing 'occurred_at'")

        return cls(
            id=product_id,
            title=data["title"],
            seller_id=data["seller_id"],
            status=data.get("status", "UNKNOWN"),
            occurred_at=datetime.fromisoformat(occurred_at),
        )
