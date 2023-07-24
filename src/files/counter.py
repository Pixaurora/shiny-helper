from typing import Self, TypedDict

from .json import SaveableToJSON
from .locations import get_counter_location


class CounterInfo(TypedDict):
    count: int


class Counter(SaveableToJSON[CounterInfo]):
    count: int

    def __init__(self, count: int) -> None:
        self.count = count

    @classmethod
    def from_data(cls, data: CounterInfo) -> Self:
        return cls(**data)

    @staticmethod
    def default_data() -> CounterInfo:
        return {'count': 0}

    @property
    def data(self) -> CounterInfo:
        return {'count': self.count}

    @classmethod
    def loaded_from_name(cls, name: str) -> Self:
        return cls.loaded_from(get_counter_location(name))
