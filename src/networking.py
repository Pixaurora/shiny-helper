import json

import aiohttp
from typing_extensions import Self

from .errors import NetworkingException


class GraphQLSession(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def query_graphql(self, url: str, query: str, **query_args: str | int):
        graphql_query = {'query': query, 'variables': query_args}

        async with self.post(
            url, data=json.dumps(graphql_query), headers={'Content-Type': 'application/json', 'X-Method-Used': 'graphiql'}
        ) as response:
            if response.status != 200:
                raise NetworkingException(response)
            try:
                data = (await response.json())['data']
            except KeyError:
                raise NetworkingException(response, 'JSON data did not have "data" field.')

        return data

    async def __aenter__(self) -> Self:
        return self
