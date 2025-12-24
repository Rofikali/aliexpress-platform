import pytest


@pytest.mark.django_db
def test_create_product_api(client):
    response = client.post("/api/v1/products/", {"name": "MacBook", "price": 1000})

    assert response.status_code == 201
