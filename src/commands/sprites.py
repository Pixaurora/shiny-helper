from ..pokeapi import PokeAPIClient, gen_7_games
from .base import NamedCommand


class PokemonSpriteCommand(NamedCommand):
    pokemon_name: str

    @property
    def name(self) -> str:
        return 'getPokemonSprite'

    async def main(self) -> None:
        async with PokeAPIClient(gen_7_games[0]) as client:
            sprites = await client.get_sprite_images(self.pokemon_name)

        print('Success! Sprites should be in cache.')
