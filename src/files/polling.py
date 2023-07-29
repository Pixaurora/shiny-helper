import asyncio
from pathlib import Path
from typing import Any, Callable, Coroutine, NoReturn

from ..errors import InvalidLocationType
from .locations import ready_to_be_file

UpdateFunction = Callable[[], Coroutine[Any, Any, None]]


class FilePoller:
    file_to_poll: Path
    remembered_file_time: float | bool

    polling_delay: float

    update_function: UpdateFunction | None

    def __init__(self, path: Path, polling_rate: int, update_function: UpdateFunction | None = None) -> None:
        if not ready_to_be_file(path):
            raise InvalidLocationType(path)

        self.file_to_poll = path
        self.remembered_file_time = self.get_modified_time()

        self.polling_delay = 1 / polling_rate

        self.update_function = update_function

    def on_update(self, update_function: UpdateFunction) -> UpdateFunction:
        self.update_function = update_function

        return update_function

    def get_modified_time(self) -> float | bool:
        return self.file_to_poll.exists() and self.file_to_poll.stat().st_mtime

    async def poll_once(self) -> None:
        assert self.update_function is not None

        newest_file_time: float | bool = self.get_modified_time()

        if newest_file_time != self.remembered_file_time:
            await self.update_function()

            self.remembered_file_time = newest_file_time

    async def poll_forever(self) -> NoReturn:
        while True:
            await self.poll_once()

            await asyncio.sleep(self.polling_delay)
