from .base import BaseCommand, NamedCommand
from .increment_hunt import IncrementHuntCommand
from .init_hunt import InitializeHuntCommand
from .ui import UICommand
from .wild_moves import GetPokemonMovesCommand

commands: list[NamedCommand] = [UICommand(), IncrementHuntCommand(), InitializeHuntCommand(), GetPokemonMovesCommand()]
command_mapping: dict[str, NamedCommand] = {command.name: command for command in commands}


class ShinyHelperCommand(BaseCommand):
    def parse_args(self) -> None:
        super().parse_args(known_only=True)

    def _get_program_choices(self) -> list[str]:
        return [command.name for command in commands]

    async def main(self) -> None:
        command: NamedCommand = command_mapping[self.command_name]

        await command.run()
