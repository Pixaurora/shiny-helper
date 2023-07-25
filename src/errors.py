from aiohttp import ClientResponse


class NetworkingException(Exception):
    response: ClientResponse

    def __init__(self, response: ClientResponse, *args: object) -> None:
        self.response = response
        super().__init__(*args)


class PokemonNotFound(Exception):
    def __init__(self, pokemon_name: str):
        super().__init__(f'{pokemon_name} not found!')


class InvalidSaveLocation(Exception):
    ...


class NonAlphanumericString(Exception):
    ...


class NoOptionSelected(Exception):
    def __init__(self):
        super().__init__('You must select an option!')
