class BaseAggregate:
    def __init__(self, aggregate_id):
        self.id = aggregate_id
        self._events = []

    def raise_event(self, event):
        self._events.append(event)

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events
