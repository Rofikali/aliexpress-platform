# filename : core/domains/products/application/ports/outbound/product_search_port.py
# from abc import ABC, abstractmethod


# class ProductSearchPort(ABC):
#     @abstractmethod
#     def search(self, filters: dict) -> list[dict]: ...

from abc import ABC, abstractmethod


class ProductSearchPort(ABC):
    @abstractmethod
    def search(
        self,
        *,
        query: str | None,
        seller_id: str | None,
        title: str | None,
        price: float | None,
    ) -> list[dict]: ...
