from django.urls import include, path

from rest_framework.routers import DefaultRouter


from core.domains.products.adapters.inbound.rest.views.product_search_viewset import (
    ProductSearchViewSet,
)
from core.domains.products.adapters.inbound.rest.views.product_view import (
    CreateProductViewSet,
)


router = DefaultRouter()

router.register(
    r"products/search",
    ProductSearchViewSet,
    basename="product-search",
)
router.register(
    r"create-products",
    CreateProductViewSet,
    basename="create-product",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router.urls)),
]
