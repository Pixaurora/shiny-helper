from typing import TypedDict

from .json import SaveableAsJSON


class CounterInfo(TypedDict):
    count: int


class Counter(SaveableAsJSON[CounterInfo]):
    @property
    def count(self) -> int:
        return self.data['count']

    @count.setter
    def count(self, new_count: int) -> None:
        self.data['count'] = new_count
