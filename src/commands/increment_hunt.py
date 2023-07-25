from pathlib import Path

from ..files import AlphanumericString, Counter, FilePoller
from .base import NamedCommand


class IncrementHuntCommand(NamedCommand):
    increment: int = 1
    hunt_name: AlphanumericString

    signal_file: Path = Path('./watched')
    polling_rate: int = 10

    @property
    def name(self) -> str:
        return 'incrementHunt'

    async def main(self) -> None:
        poller = FilePoller(self.signal_file, self.polling_rate)

        hunt = Counter.loaded_from_name(self.hunt_name)

        @poller.on_update
        async def on_update() -> None:
            hunt.count += self.increment
            hunt.save()

            print(f'{self.hunt_name} encounters: {hunt.count - self.increment} -> {hunt.count}')

        print(f'Hunt {self.hunt_name} is currently at {hunt.count} encounters total.')
        print(f'Run `touch {self.signal_file.absolute()}` in a different shell to increment the hunt!')

        await poller.poll_forever()
