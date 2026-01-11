# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response

# from core.domains.products.application.use_cases.search_products.search_products_query import (
#     SearchProductsQuery,
# )
# from core.domains.products.adapters.outbound.search.product_search_es_adapter import (
#     ProductSearchElasticsearchAdapter,
# )

# # from .serializers.product_search_serializer import ProductSearchSerializer
# from core.domains.products.adapters.inbound.rest.serializers.product_search_serializer import (
#     ProductSearchSerializer,
# )


# class ProductSearchViewSet(ViewSet):
#     """
#     Product search (CQRS / Read Model) ViewSet
#     """

#     def list(self, request):
#         query = request.query_params.get("q")
#         seller_id = request.query_params.get("seller_id")

#         search_port = ProductSearchElasticsearchAdapter()
#         use_case = SearchProductsQuery(search_port)

#         results = use_case.execute(
#             query=query,
#             seller_id=seller_id,
#         )

#         serializer = ProductSearchSerializer(results, many=True)
#         return Response(serializer.data)


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from core.domains.products.application.use_cases.search_products.search_products_query import (
    SearchProductsQuery,
)


class ProductSearchViewSet(ViewSet):
    def list(self, request):
        title = request.query_params.get("title")

        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        query = SearchProductsQuery(
            title=title,
            min_price=float(min_price) if min_price else None,
            max_price=float(max_price) if max_price else None,
        )

        results = query.execute()

        return Response(
            {
                "count": len(results),
                "results": results,
            },
            status=status.HTTP_200_OK,
        )
