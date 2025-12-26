from core.shared.observability.metrics import orders_failed_total


def handle_payment_failed(event):
    orders_failed_total.inc()
