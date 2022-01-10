from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Callable, Dict, List, Type

from fractal.core.command_bus.command import Command
from fractal.core.event_sourcing.event import (
    BasicSendingEvent,
    Event,
    EventCommandMapper,
)


def get_all():
    return [
        ProductAddedEvent,
        ProductUpdatedEvent,
        ProductDeletedEvent,
    ]


@dataclass
class ProductEvent(BasicSendingEvent):
    id: str

    @property
    def object_id(self):
        return self.id

    @property
    def aggregate_root_id(self):
        return self.id


@dataclass
class ProductAddedEvent(ProductEvent):
    account_id: str
    name: str
    price: Decimal
    created_by: str
    created_on: datetime


@dataclass
class ProductUpdatedEvent(ProductEvent):
    account_id: str
    name: str
    price: Decimal
    updated_by: str
    updated_on: datetime


@dataclass
class ProductDeletedEvent(ProductEvent):
    pass


class ProductEventCommandMapper(EventCommandMapper):
    def mappers(self) -> Dict[Type[Event], List[Callable[[Event], Command]]]:
        return {}
