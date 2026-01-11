import logging
from core.domains.products.read_model.documents.product_search_document import (
    ProductSearchDocument,
)


class ProductEventProjection:
    logging.debug(
        "Product Event Projection : "
        "core/domains/products/read_model/projections/product_event_projection.py"
    )

    def __init__(self, es_client):
        self.es = es_client

    def handle(
        self,
        payload: dict,
        metadata: dict,
        *,
        index_name: str | None = None,
        index_alias: str | None = None,
    ):
        if not index_name and not index_alias:
            raise ValueError("Either index_name or index_alias must be provided")

        document = ProductSearchDocument.from_event(payload, metadata)

        target = index_name or index_alias

        self.es.index(
            index=target,
            id=document.id,
            document=document.to_dict(),
        )
