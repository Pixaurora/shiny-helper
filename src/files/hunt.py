from pathlib import Path
from typing import Self, TypedDict

from .json import SaveableToJSON
from .locations import POLLED_FILES, get_hunt_location, get_name_from_path
from .polling import FilePoller, UpdateFunction


class HuntInfo(TypedDict):
    species: str

    encounters: int


class Hunt(SaveableToJSON[HuntInfo]):
    species: str

    encounters: int

    def __init__(self, species: str, encounters: int) -> None:
        self.species = species
        self.encounters = encounters

    @classmethod
    def from_data(cls, data: HuntInfo) -> Self:
        return cls(**data)

    @staticmethod
    def default_data() -> HuntInfo:
        return {'species': 'pikachu', 'encounters': 0}

    @property
    def data(self) -> HuntInfo:
        return { 'species': self.species, 'encounters': self.encounters}

    @classmethod
    def loaded_from_name(cls, name: str) -> Self:
        return cls.loaded_from(get_hunt_location(name))

    @property
    def name(self) -> str:
        return get_name_from_path(self.location)

    @name.setter
    def name(self, new_name: str) -> None:
        self.location = get_hunt_location(new_name)

    def create_poller(
        self, watched_file: Path | None = None, polling_rate: int = 5, update_function: UpdateFunction | None = None
    ) -> FilePoller:
        if watched_file is None:
            watched_file = POLLED_FILES / self.name

        return FilePoller(watched_file, polling_rate, update_function)
