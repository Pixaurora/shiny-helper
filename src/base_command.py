from abc import ABC, abstractmethod

from tap import Tap


class BaseCommand(ABC, Tap):
    command: str

    def __init__(self) -> None:
        super().__init__(underscores_to_dashes=True)

    def configure(self) -> None:
        self.add_argument('command', choices=self._get_program_choices())

    def _get_program_choices(self) -> list[str]:
        return list(command_mapping.keys())

    async def run(self) -> None:
        self.parse_args()

        await self.main()

    @abstractmethod
    async def main(self) -> None:
        ...


command_mapping: dict[str, type[BaseCommand]] = {}


def command(name: str):
    def add_command(command_type: type[BaseCommand]) -> type[BaseCommand]:
        def _get_program_choices(self) -> list[str]:
            return [name]

        command_type._get_program_choices = _get_program_choices

        command_mapping[name] = command_type

        return command_type

    return add_command
