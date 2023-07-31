from ..files import AlphanumericString, Hunt
from .base import NamedCommand


class InitializeHuntCommand(NamedCommand):
    species: str
    first_value: int = 0

    hunt_name: AlphanumericString

    @property
    def name(self) -> str:
        return 'initHunt'

    async def main(self) -> None:
        new_hunt: Hunt = Hunt(self.species, self.first_value)
        new_hunt.name = self.hunt_name

        new_hunt.save()

        print('New hunt successfully initialized!')
