import httpx
from httpx import Client
from typing_extensions import Self

from ..errors import NetworkingException


class GraphQLClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def query_graphql(self, url: str, query: str, **query_args: str | int) -> dict:
        graphql_query = {'query': query, 'variables': query_args}

        response: httpx.Response = self.post(
            url, json=graphql_query, headers={'Content-Type': 'application/json', 'X-Method-Used': 'graphiql'}
        )

        if response.status_code != 200:
            raise NetworkingException(response)
        try:
            data: dict = response.json()['data']
        except KeyError:
            raise NetworkingException(response, 'JSON data did not have "data" field.')

        return data

    async def __aenter__(self) -> Self:
        return self
