from core.shared.tests.integration.event_utils import publish_event, wait_for_index
import pytest

payload = {
    "id": "prod-123",
    "name": "Smartphone",
    "price": 699,
}


def test_product_indexed_in_es(kafka, elastic):
    publish_event("product.created", payload)

    wait_for_index("product_search", payload["id"])
