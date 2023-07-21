from .base import BaseCommand, NamedCommand
from .increment_hunt import IncrementHunt
from .init_hunt import InitializeHunt
from .wild_moves import GetPokemonMoves

commands: list[NamedCommand] = [IncrementHunt(), InitializeHunt(), GetPokemonMoves()]
command_mapping: dict[str, NamedCommand] = {command.name: command for command in commands}


class ShinyHelper(BaseCommand):
    def parse_args(self) -> None:
        super().parse_args(known_only=True)

    def _get_program_choices(self) -> list[str]:
        return [command.name for command in commands]

    async def main(self) -> None:
        command: NamedCommand = command_mapping[self.command_name]

        await command.run()
