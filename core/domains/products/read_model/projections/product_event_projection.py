# # core/domains/products/read_model/projections/product_event_projection.py
# # from core.shared.infrastructure.elasticsearch_client import get_es_client
# # from core.domains.products.read_model.documents.product_search_document import (
# #     ProductSearchDocument,
# # )


# # class ProductEventProjection:
# #     INDEX = "product_search_v1"

# #     def index(self, payload: dict, metadata: dict) -> None:
# #         document = ProductSearchDocument.from_event(payload, metadata)
# #         es = get_es_client()

# #         es.index(
# #             index=self.INDEX,
# #             id=document.id,
# #             document=document.__dict__,
# #         )

# #     def delete(self, payload: dict) -> None:
# #         product_id = payload.get("product_id")
# #         if not product_id:
# #             raise ValueError("product_id required for delete projection")

# #         es = get_es_client()
# #         es.delete(index=self.INDEX, id=product_id, ignore=[404])

# from core.shared.infrastructure.elasticsearch_client import get_es_client
# from core.domains.products.read_model.documents.product_search_document import (
#     ProductSearchDocument,
# )

# import logging


# class ProductEventProjection:
#     INDEX = "product_search_v1"

#     def index(self, payload: dict, metadata: dict):
#         es = get_es_client()

#         document = ProductSearchDocument.from_event(payload, metadata)
#         logging.debug(f"Indexing document in Elasticsearch: {document}")

#         es.index(
#             index=self.INDEX,
#             id=document.id,
#             document={
#                 "title": document.title,
#                 "price": document.price,
#                 "created_at": document.occurred_at.isoformat(),
#             },
#         )

#     def delete(self, product_id: str):
#         es = get_es_client()
#         es.delete(index=self.INDEX, id=product_id, ignore=[404])


from core.shared.infrastructure.elasticsearch_client import get_es_client
from core.domains.products.read_model.documents.product_search_document import (
    ProductSearchDocument,
)


class ProductEventProjection:
    INDEX = "product_search_v1"

    def index(self, payload: dict, metadata: dict):
        es = get_es_client()

        doc = ProductSearchDocument.from_event(payload, metadata)

        es.index(
            index=self.INDEX,
            id=doc.id,
            document={
                "title": doc.title,
                "seller_id": doc.seller_id,
                "status": doc.status,
                "occurred_at": doc.occurred_at.isoformat(),
            },
        )

    def delete(self, product_id: str):
        es = get_es_client()
        es.delete(index=self.INDEX, id=product_id, ignore=[404])
