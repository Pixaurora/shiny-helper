import json

from ..errors import PokemonNotFound
from ..files import get_image_from_cache, put_image_into_cache
from .games import Game
from .graphql import GraphQLClient
from .pokemon_data import Move
from .sprites import SPRITE_MAPPING


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

    async def get_sprite_locations(self, pokemon_name: str) -> dict[str, str]:
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

        relevant_links: dict[str, str] = {
            sprite_type: all_sprite_links[json_key] for sprite_type, json_key in SPRITE_MAPPING.items()
        }

        for sprite_type in relevant_links:
            link: str = relevant_links[sprite_type]
            fixed_link: str = link[1:] if link[0] == '/' else link

            relevant_links[sprite_type] = fixed_link

        return relevant_links

    async def get_sprite_image(self, link: str) -> bytes:
        cached_image: bytes | None = get_image_from_cache(link)

        if cached_image is not None:
            return cached_image

        remote_link: str = link.replace('media', 'https://raw.githubusercontent.com/PokeAPI/sprites/master')

        async with self.get(remote_link) as response:
            image: bytes = await response.read()
            put_image_into_cache(link, image)

            return image

    async def get_sprite_images(self, pokemon_name: str) -> dict[str, bytes]:
        relevant_links: dict[str, str] = await self.get_sprite_locations(pokemon_name)

        return {sprite_type: await self.get_sprite_image(link) for sprite_type, link in relevant_links.items()}
