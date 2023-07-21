from typing import TypedDict

from ..errors import PokemonNotFound
from .games import Game
from .graphql import GraphQLClient


class Move(TypedDict):
    name: str
    pp: int


class PokeAPIClient(GraphQLClient):
    game: Game

    def __init__(self, game: Game, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game = game

    def get_if_pokemon_exists(self, pokemon_name: str) -> bool:
        data = self.query_graphql(
            'https://beta.pokeapi.co/graphql/v1beta',
            """
            query pokemonExists($pokemon_name: String) {
                species: pokemon_v2_pokemon(where: {name: {_eq: $pokemon_name}}) {
                    pokemon_species_id
                }
            }
            """,
            pokemon_name=pokemon_name,
        )

        return len(data['species']) > 0

    def get_wild_moveset(self, pokemon_name: str, level: int) -> list[Move]:
        exists = self.get_if_pokemon_exists(pokemon_name)

        if not exists:
            raise PokemonNotFound(pokemon_name)

        data = self.query_graphql(
            'https://beta.pokeapi.co/graphql/v1beta',
            """
            query getWildMoveset($game_name: String, $pokemon_name: String, $level: Int) {
                known_moves: pokemon_v2_pokemonmove(
                    where: {
                        pokemon_v2_pokemon: {
                            name: {_eq: $pokemon_name}
                        },
                        pokemon_v2_movelearnmethod: {
                            name: {_eq: "level-up"}
                        },
                        level: {_lte: $level},
                        pokemon_v2_versiongroup: {
                            name: {_eq: $game_name}
                        }
                    },
                    order_by: {level: desc},
                    limit: 4
                ) {
                    pokemon_v2_move {
                        name
                        pp
                    }
                }
            }
            """,
            game_name=self.game.api_name,
            pokemon_name=pokemon_name,
            level=level,
        )

        return [move['pokemon_v2_move'] for move in data['known_moves']]
