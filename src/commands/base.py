from abc import ABC, abstractmethod

from tap import Tap


class BaseCommand(ABC, Tap):
    command_name: str

    def __init__(self) -> None:
        super().__init__(underscores_to_dashes=True)

    def configure(self) -> None:
        self.add_argument('command_name', choices=self._get_program_choices())

    @abstractmethod
    def _get_program_choices(self) -> list[str]:
        ...

    def run(self) -> None:
        self.parse_args()

        self.main()

    @abstractmethod
    def main(self) -> None:
        ...


class NamedCommand(BaseCommand):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    def _get_program_choices(self) -> list[str]:
        return [self.name]
