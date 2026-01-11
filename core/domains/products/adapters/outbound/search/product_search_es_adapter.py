# filename : core/domains/products/adapters/outbound/search/product_search_es_adapter.py

# from core.shared.infrastructure.search.elasticsearch_client import get_es_client
# import logging

# PRODUCT_SEARCH_ALIAS = "product_search_current"


# class ProductSearchElasticsearchAdapter:
#     logging.debug("ProductSearchElasticsearchAdapter initialized.")

#     def __init__(self):
#         self.es = get_es_client()

#     def search(self, filters: dict):
#         query = {"query": {"match": {"name": filters.get("q", "")}}}

#         result = self.es.search(
#             index=PRODUCT_SEARCH_ALIAS,  # 🔥 ALIAS ONLY
#             body=query,
#         )

#         return [hit["_source"] for hit in result["hits"]["hits"]]


from core.shared.infrastructure.search.elasticsearch_client import get_es_client
import logging

PRODUCT_SEARCH_ALIAS = "product_search_current"


class ProductSearchElasticsearchAdapter:
    logging.debug("ProductSearchElasticsearchAdapter initialized.")

    def __init__(self):
        self.es = get_es_client()

    def search(
        self,
        *,
        query: str | None,
        seller_id: str | None,
        title: str | None,
        price: float | None,
    ):
        must = []

        if query:
            must.append({"match": {"title": query}})

        if seller_id:
            must.append({"term": {"seller_id": seller_id}})

        if title:
            must.append({"match": {"title": title}})

        if price is not None:
            must.append({"term": {"price": price}})

        body = {
            "query": {"bool": {"must": must or {"match_all": {}}}},
            "sort": [{"occurred_at": "desc"}],
            
        }

        response = self.es.search(
            index=PRODUCT_SEARCH_ALIAS,  # 🔥 ALIAS ONLY
            body=body,
        )

        return [hit["_source"] for hit in response["hits"]["hits"]]
