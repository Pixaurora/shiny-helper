from pathlib import Path

from ..files import AlphanumericString, FilePoller, Hunt
from .base import NamedCommand


class IncrementHuntCommand(NamedCommand):
    increment: int = 1
    hunt_name: AlphanumericString

    watched_file: Path | None = None
    polling_rate: int = 5

    @property
    def name(self) -> str:
        return 'incrementHunt'

    async def main(self) -> None:
        hunt = Hunt.loaded_from_name(self.hunt_name)

        poller: FilePoller = hunt.create_poller(self.watched_file, self.polling_rate)

        @poller.on_update
        async def on_update() -> None:
            hunt.count += self.increment
            hunt.save()

            print(f'{hunt.name} encounters: {hunt.count - self.increment} -> {hunt.count}')

        print(f'Hunt {self.hunt_name} is currently at {hunt.count} encounters total.')
        print(f'Run `touch {poller.file_to_poll.absolute()}` in a different shell to increment the hunt!')

        await poller.poll_forever()
