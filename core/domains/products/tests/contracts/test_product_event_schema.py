from core.domains.products.tests.factories import build_product_created_event
import pytest


def test_product_created_event_schema():
    event = build_product_created_event()

    assert "id" in event["payload"]
    assert "name" in event["payload"]
    assert "email" not in event["payload"]
