from pathlib import Path

from aiohttp import ClientResponse
from textual.widgets import OptionList


class NetworkingException(Exception):
    response: ClientResponse

    def __init__(self, response: ClientResponse, *args: object) -> None:
        super().__init__(*args)

        self.response = response


class PokemonNotFound(Exception):
    pokemon_name: str

    def __init__(self, pokemon_name: str) -> None:
        super().__init__(f'{pokemon_name} not found!')

        self.pokemon_name = pokemon_name


class InvalidLocationType(Exception):
    offending_location: Path

    def __init__(self, location: Path) -> None:
        super().__init__(f'Location must be a file and exist.')

        self.offending_location = location


class NonAlphanumericString(Exception):
    offending_string: str

    def __init__(self, offending_string: str) -> None:
        super().__init__('Alphanumeric strings must contain only letters and numbers.')

        self.offending_string = offending_string


class NoOptionSelected(Exception):
    selector: OptionList

    def __init__(self, selector: OptionList) -> None:
        super().__init__('You must select an option!')

        self.selector = selector
