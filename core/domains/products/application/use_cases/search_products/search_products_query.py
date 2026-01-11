# # filename : core/domains/products/application/use_cases/search_products/search_products_query.py
# # class SearchProductsQuery:
# #     def __init__(self, search_port):
# #         self.search_port = search_port

# #     def execute(self, filters: dict):
# #         return self.search_port.search(filters)


# class SearchProductsQuery:
#     def __init__(self, search_port):
#         self.search_port = search_port

#     def execute(
#         self,
#         *,
#         query: str | None,
#         seller_id: str | None,
#         title: str | None,
#         price: float | None,
#     ):
#         return self.search_port.search(
#             query=query,
#             seller_id=seller_id,
#             title=title,
#             price=price,
#         )


from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class SearchProductsQuery:
    title: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    def execute(self) -> List[dict]:
        """
        Pure application-level query.
        No HTTP, no DRF, no Elasticsearch client logic here.
        """
        from core.domains.products.read_model.repositories.product_search_repository import (
            ProductSearchRepository,
        )

        repo = ProductSearchRepository()
        return repo.search(
            title=self.title,
            min_price=self.min_price,
            max_price=self.max_price,
        )
