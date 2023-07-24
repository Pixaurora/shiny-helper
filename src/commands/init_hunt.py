from pathlib import Path

from ..files import AlphanumericString, Counter, get_counter_location
from .base import NamedCommand


class InitializeHuntCommand(NamedCommand):
    first_value: int = 0
    hunt_name: AlphanumericString

    @property
    def name(self) -> str:
        return 'initHunt'

    async def main(self) -> None:
        new_counter: Counter = Counter.from_data({'count': self.first_value})

        save_location: Path = get_counter_location(self.hunt_name)
        new_counter.save(save_location)

        print('New hunt successfully initialized!')
