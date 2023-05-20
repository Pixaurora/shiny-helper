import os
import re
from pathlib import Path

from desktop_notifier import DesktopNotifier, Notification

from .base_command import BaseCommand, command, command_mapping
from .counter import Counter
from .errors import NonAlphanumericString


class AlphanumericString(str):
    def __init__(self, data: object) -> None:
        self = str(data)

        if re.fullmatch(r'[\w\d]*', self) is None:
            raise NonAlphanumericString('Alphanumeric strings must contain only letters and numbers.')


hunt_path: Path = Path.home().joinpath('.config/shiny-helper/counters/')


def get_counter_location(hunt_name: str) -> Path:
    return hunt_path.joinpath(f'{hunt_name}.json')


notifier = DesktopNotifier('Shiny Helper')


@command('initHunt')
class InitializeHunt(BaseCommand):
    first_value: int = 0
    hunt_name: AlphanumericString

    async def main(self) -> None:
        new_counter: Counter = Counter()
        new_counter.data = {'count': self.first_value}

        save_location: Path = get_counter_location(self.hunt_name)
        os.makedirs(hunt_path, exist_ok=True)

        await new_counter.save(save_location)

        print('New hunt successfully initialized!')


@command('incrementHunt')
class IncrementHunt(BaseCommand):
    increment: int = 1
    hunt_name: AlphanumericString

    notify: bool = False

    async def main(self) -> None:
        async with Counter(get_counter_location(self.hunt_name)) as counter:
            old_count: int = counter.count
            counter.count += self.increment
            new_count: int = counter.count

        title: str = f'{self.hunt_name} encounters'
        message: str = f'{old_count} -> {new_count}'

        if self.notify:
            await notifier.send_notification(Notification(title, message))
        else:
            print(f'{title}: {message}')


class ShinyHelper(BaseCommand):
    def parse_args(self) -> None:
        super().parse_args(known_only=True)

    async def main(self) -> None:
        type_of_command: type[BaseCommand] = command_mapping[self.command]
        command: BaseCommand = type_of_command()

        await command.run()
