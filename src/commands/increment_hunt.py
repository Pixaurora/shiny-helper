from pathlib import Path

from ..files import AlphanumericString, Counter, FilePoller, get_counter_location
from .base import NamedCommand


class IncrementHunt(NamedCommand):
    increment: int = 1
    hunt_name: AlphanumericString

    signal_file: Path = Path('./watched')
    polling_rate: int = 10

    @property
    def name(self) -> str:
        return 'incrementHunt'

    async def main(self) -> None:
        poller = FilePoller(self.signal_file, self.polling_rate)

        @poller.on_update
        async def on_update() -> None:
            with Counter(get_counter_location(self.hunt_name)) as counter:
                counter.count += self.increment
                new_count: int = counter.count

            print(f'{self.hunt_name} encounters: {new_count - self.increment} -> {new_count}')

        with Counter(get_counter_location(self.hunt_name)) as hunt:
            print(f'Hunt {self.hunt_name} is currently at {hunt.count} encounters total.')
            print(f'Run `touch {self.signal_file.absolute()}` in a different shell to increment the hunt!')

        await poller.poll()
