from core.shared.infrastructure.outbox_writer import write_event
from core.shared.models.outbox import Outbox

def test_outbox_event_written(db):
    write_event(
        aggregate_type="product",
        aggregate_id="prod-1",
        event_type="product.created",
        payload={"name": "TV"},
    )

    assert Outbox.objects.count() == 1
