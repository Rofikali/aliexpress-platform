# filename : core/shared/kernel/domain_event.py
from abc import ABC

# from json import dumps
from uuid import UUID
from datetime import datetime


class DomainEvent(ABC):
    aggregate_id: UUID
    occurred_at: datetime

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

    def to_primitives(self) -> dict:
        raise NotImplementedError

    # def to_json(self) -> str:
    #     return dumps(self.to_primitives())
