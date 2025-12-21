from datetime import datetime
import uuid

class DomainEvent:
    event_id = uuid.uuid4()

    def __init__(self, aggregate_id):
        self.aggregate_id = aggregate_id
        self.occurred_at = datetime.utcnow()
