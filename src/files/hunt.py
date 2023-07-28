from typing import Self, TypedDict

from .json import SaveableToJSON
from .locations import get_hunt_location, get_name_from_path


class HuntInfo(TypedDict):
    count: int


class Hunt(SaveableToJSON[HuntInfo]):
    count: int

    def __init__(self, count: int) -> None:
        self.count = count

    @classmethod
    def from_data(cls, data: HuntInfo) -> Self:
        return cls(**data)

    @staticmethod
    def default_data() -> HuntInfo:
        return {'count': 0}

    @property
    def data(self) -> HuntInfo:
        return {'count': self.count}

    @classmethod
    def loaded_from_name(cls, name: str) -> Self:
        return cls.loaded_from(get_hunt_location(name))

    @property
    def name(self) -> str:
        return get_name_from_path(self.location)

    @name.setter
    def name(self, new_name: str) -> None:
        self.location = get_hunt_location(new_name)
