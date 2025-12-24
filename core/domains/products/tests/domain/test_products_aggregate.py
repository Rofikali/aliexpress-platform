import pytest
from core.domains.products.domain.aggregates.product_aggregate import ProductAggregate
from core.domains.products.domain.value_objects.product_status import ProductStatus


def test_product_can_be_published():
    product = ProductAggregate.create(name="iPhone", seller_id="seller-123")

    product.publish()

    assert product.status == ProductStatus.PUBLISHED
    assert product.has_event("product.published")
