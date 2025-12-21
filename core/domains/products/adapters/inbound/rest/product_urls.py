from django.urls import path
from .product_views import CreateProductView

urlpatterns = [
    path("products/", CreateProductView.as_view()),
]
