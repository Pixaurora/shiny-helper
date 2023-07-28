import re
from pathlib import Path

from ..errors import NonAlphanumericString

program_config: Path = Path.home() / '.config/shiny-helper'
hunt_path: Path = program_config / 'counters'


class AlphanumericString(str):
    def __init__(self, data: object) -> None:
        self = str(data)

        if re.fullmatch(r'[\w\d]*', self) is None:
            raise NonAlphanumericString('Alphanumeric strings must contain only letters and numbers.')


def get_hunt_location(hunt_name: str) -> Path:
    return hunt_path / f'{hunt_name}.json'


def get_name_from_path(location: Path) -> str:
    return location.name.replace(location.suffix, '')


def get_hunt_names() -> list[str]:
    assert hunt_path.is_dir() or not hunt_path.exists()
    hunt_path.mkdir(parents=True, exist_ok=True)

    return [get_name_from_path(path) for path in hunt_path.iterdir() if path.is_file()]
