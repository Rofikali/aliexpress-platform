from core.domains.products.tests.saga.checkout_saga_utils import (
    create_order,
    confirm_payment,
    reserve_inventory,
    order_status,
)
import pytest


def test_checkout_saga_success():
    create_order()
    confirm_payment()
    reserve_inventory()

    assert order_status() == "CONFIRMED"
