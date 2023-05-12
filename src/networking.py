import json
from typing import Any

import aiohttp

from .errors import NetworkingException


async def do_graphql_request(query: str, **query_args: str | int):
    async with aiohttp.ClientSession() as session:
        graphql_query = {'query': query, 'variables': query_args}

        async with session.post(
            'https://beta.pokeapi.co/graphql/v1beta',
            data=json.dumps(graphql_query),
            headers={'Content-Type': 'application/json', 'X-Method-Used': 'graphiql'},
        ) as response:
            if response.status != 200:
                raise NetworkingException(response)
            try:
                data = (await response.json())['data']
            except KeyError:
                raise NetworkingException(response, 'JSON data did not have "data" field.')

    return data
