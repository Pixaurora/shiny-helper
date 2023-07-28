import json
from pathlib import Path
from typing import Generic, Protocol, Self, TypedDict, TypeVar

from ..errors import InvalidLocationType
from .locations import ready_to_be_file

D = TypeVar('D', bound=TypedDict)


class SerializableToDict(Protocol, Generic[D]):
    @staticmethod
    def default_data() -> D:
        ...

    @property
    def data(self) -> D:
        ...

    @classmethod
    def from_data(cls, data: D) -> Self:
        ...

    @classmethod
    def fix_data(cls, data: dict) -> D:
        new_data: D = cls.default_data()
        new_data.update(data)  # type: ignore

        return new_data


class SaveableToJSON(SerializableToDict[D], Protocol):
    __location: Path | None = None

    @property
    def location(self) -> Path:
        assert self.__location is not None
        return self.__location

    @location.setter
    def location(self, new_location) -> None:
        if not ready_to_be_file(new_location):
            raise InvalidLocationType(new_location)

        self.__location = new_location

    def save(self, new_location: Path | None = None) -> None:
        if new_location is not None:
            self.location = new_location

        with open(self.location, 'w') as file:
            file.write(json.dumps(self.data))

    @classmethod
    def loaded_from(cls, location: Path) -> Self:
        if not location.is_file():
            raise InvalidLocationType(location)

        with open(location, 'r') as file:
            data: dict = json.load(file)

        object: Self = cls.from_data(cls.fix_data(data))
        object.location = location

        return object
