import json

from ..errors import PokemonNotFound
from .games import Game
from .graphql import GraphQLClient
from .pokemon_data import Move
from .sprites import SpriteForms


class PokeAPIClient(GraphQLClient):
    game: Game

    def __init__(self, game: Game, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game = game

    async def get_if_pokemon_exists(self, pokemon_name: str) -> bool:
        data = await self.query_graphql(
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

    async def get_wild_moveset(self, pokemon_name: str, level: int) -> list[Move]:
        exists: bool = await self.get_if_pokemon_exists(pokemon_name)

        if not exists:
            raise PokemonNotFound(pokemon_name)

        data = await self.query_graphql(
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

    async def get_sprite_locations(self, pokemon_name: str) -> SpriteForms[str]:
        exists: bool = await self.get_if_pokemon_exists(pokemon_name)

        if not exists:
            raise PokemonNotFound(pokemon_name)

        data = await self.query_graphql(
            'https://beta.pokeapi.co/graphql/v1beta',
            """
            query getWildMoveset($pokemon_name: String) {
            found_sprites: pokemon_v2_pokemonsprites(where: {pokemon_v2_pokemon: {name: {_eq: $pokemon_name}}}) {
                sprites
            }
            }
            """,
            pokemon_name=pokemon_name,
        )

        all_sprite_links: dict = json.loads(data['found_sprites'][0]['sprites'])

        relevant_links: SpriteForms[str] = {'normal': all_sprite_links['front_default'], 'shiny': all_sprite_links['front_shiny']}

        for sprite_type in relevant_links:
            link: str = relevant_links[sprite_type]
            fixed_link: str = link[1:] if link[0] == '/' else link

            relevant_links[sprite_type] = fixed_link

        return relevant_links
