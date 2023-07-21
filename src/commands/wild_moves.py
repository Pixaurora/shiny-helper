from ..pokeapi import Move, PokeAPIClient, gen_7_games
from .base import NamedCommand


class GetPokemonMoves(NamedCommand):
    pokemon_name: str
    level: int

    @property
    def name(self) -> str:
        return 'getPokemonMoves'

    async def main(self) -> None:
        async with PokeAPIClient(gen_7_games[0]) as client:
            moves: list[Move] = await client.get_wild_moveset(self.pokemon_name, self.level)

        print(f'Total PP: {sum(move["pp"] for move in moves)}')

        for move in moves:
            print(f'\t{move["name"]}: {move["pp"]} PP')
