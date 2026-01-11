# # filename : core/domains/products/read_model/indices/product_search_index.py
# from elasticsearch import Elasticsearch
# import logging

# logging.debug(
#     "Product Search Index : "
#     "core/domains/products/read_model/indices/product_search_index.py"
# )


# INDEX_ALIAS = "product_search"
# INDEX_VERSION = "v1"


# def index_name(version: str = INDEX_VERSION) -> str:
#     return f"{INDEX_ALIAS}_{version}"


# MAPPING = {
#     "mappings": {
#         "properties": {
#             "id": {"type": "keyword"},
#             "name": {"type": "text"},
#             "price": {"type": "double"},
#             "created_at": {"type": "date"},
#         }
#     }
# }


# def create_index(es: Elasticsearch, version: str):
#     name = index_name(version)

#     if es.indices.exists(index=name):
#         return

#     es.indices.create(
#         index=name,
#         body=MAPPING,
#     )

import logging

logging.debug(
    "Product Search Index : "
    "core/domains/products/read_model/indices/product_search_index.py"
)
PRODUCT_SEARCH_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "text"},
            "price": {"type": "float"},
            "occurred_at": {"type": "date"},
        }
    }
}
