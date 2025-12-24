from core.shared.tests.chaos.service_utils import stop_service
import pytest

def test_kafka_down(api_client):
    stop_service("kafka")

    response = api_client.post("/api/v1/orders/")
    assert response.status_code == 201  # outbox still works
