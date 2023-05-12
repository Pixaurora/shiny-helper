from typing import TypedDict

from .errors import PokemonNotFoundException
from .games import Game
from .networking import do_graphql_request


class Move(TypedDict):
    name: str
    pp: int


async def get_if_pokemon_exists(pokemon_name: str) -> bool:
    data = await do_graphql_request(
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


async def get_wild_moveset(game: Game, pokemon_name: str, level: int) -> list[Move]:
    exists = await get_if_pokemon_exists(pokemon_name)

    if not exists:
        raise PokemonNotFoundException(pokemon_name)

    data = await do_graphql_request(
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
        game_name=game.api_name,
        pokemon_name=pokemon_name,
        level=level,
    )

    return [move['pokemon_v2_move'] for move in data['known_moves']]
