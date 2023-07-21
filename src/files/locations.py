import re
from pathlib import Path

from ..errors import NonAlphanumericString

shiny_helper_config: Path = Path.home().joinpath('.config/shiny-helper')
hunt_path: Path = shiny_helper_config.joinpath('counters')


class AlphanumericString(str):
    def __init__(self, data: object) -> None:
        self = str(data)

        if re.fullmatch(r'[\w\d]*', self) is None:
            raise NonAlphanumericString('Alphanumeric strings must contain only letters and numbers.')


def get_counter_location(hunt_name: str) -> Path:
    return hunt_path.joinpath(f'{hunt_name}.json')
