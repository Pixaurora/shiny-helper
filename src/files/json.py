import json
from pathlib import Path
from typing import Generic, Protocol, Self, TypedDict, TypeVar

from ..errors import InvalidSaveLocation

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


class SaveableToJSON(SerializableToDict, Protocol, Generic[D]):
    __location: Path | None

    @property
    def location(self) -> Path:
        if self.__location is None:
            raise InvalidSaveLocation('Save location has not been set.')

        return self.__location

    @location.setter
    def location(self, new_location) -> None:
        if new_location.exists() and not new_location.is_file():
            raise InvalidSaveLocation(f'Save location must be a file, not {new_location.stat().st_mode}')

        self.__location = new_location

    def save(self, new_location: Path | None = None) -> None:
        if new_location is not None:
            self.location = new_location

        with open(self.location, 'w') as file:
            file.write(json.dumps(self.data))

    @classmethod
    def loaded_from(cls, location: Path) -> Self:
        if not location.is_file():
            raise InvalidSaveLocation('Save location must exist and be a file.')

        with open(location, 'r') as file:
            data: dict = json.load(file)

        object: Self = cls.from_data(cls.fix_data(data))
        object.location = location

        return object
