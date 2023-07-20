import os
import re
from pathlib import Path

from .base_command import BaseCommand, command, command_mapping
from .counter import Counter
from .errors import NonAlphanumericString
from .file_polling import FilePoller
from .games import gen_7_games
from .wild_pokemon import Move, PokeAPIClient


class AlphanumericString(str):
    def __init__(self, data: object) -> None:
        self = str(data)

        if re.fullmatch(r'[\w\d]*', self) is None:
            raise NonAlphanumericString('Alphanumeric strings must contain only letters and numbers.')


hunt_path: Path = Path.home().joinpath('.config/shiny-helper/counters/')


def get_counter_location(hunt_name: str) -> Path:
    return hunt_path.joinpath(f'{hunt_name}.json')


@command('initHunt')
class InitializeHunt(BaseCommand):
    first_value: int = 0
    hunt_name: AlphanumericString

    def main(self) -> None:
        new_counter: Counter = Counter()
        new_counter.data = {'count': self.first_value}

        save_location: Path = get_counter_location(self.hunt_name)
        os.makedirs(hunt_path, exist_ok=True)

        new_counter.save(save_location)

        print('New hunt successfully initialized!')


@command('incrementHunt')
class IncrementHunt(BaseCommand):
    increment: int = 1
    hunt_name: AlphanumericString

    signal_file: Path = Path('./watched')
    polling_rate: int = 10

    def main(self) -> None:
        poller = FilePoller(self.signal_file, self.polling_rate)

        @poller.on_update
        def on_update() -> None:
            with Counter(get_counter_location(self.hunt_name)) as counter:
                counter.count += self.increment
                new_count: int = counter.count

            print(f'{self.hunt_name} encounters: {new_count - self.increment} -> {new_count}')

        with Counter(get_counter_location(self.hunt_name)) as hunt:
            print(f'Hunt {self.hunt_name} is currently at {hunt.count} encounters total.')
            print(f'Run `touch {self.signal_file.absolute()}` in a different shell to increment the hunt!')

        poller.poll()


@command('getPokemonMoves')
class PokemonMoves(BaseCommand):
    pokemon_name: str
    level: int

    def main(self) -> None:
        client = PokeAPIClient(gen_7_games[0])

        moves: list[Move] = client.get_wild_moveset(self.pokemon_name, self.level)

        print(f'Total PP: {sum(move["pp"] for move in moves)}')

        for move in moves:
            print(f'\t{move["name"]}: {move["pp"]} PP')


class ShinyHelper(BaseCommand):
    def parse_args(self) -> None:
        super().parse_args(known_only=True)

    def main(self) -> None:
        type_of_command: type[BaseCommand] = command_mapping[self.command]
        command: BaseCommand = type_of_command()

        command.run()
