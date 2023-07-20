import time
from pathlib import Path
from typing import Callable, NoReturn

UpdateFunction = Callable[[], None]


class FilePoller:
    file_to_poll: Path
    polling_rate: int

    update_function: UpdateFunction | None

    def __init__(self, path: Path, polling_rate: int) -> None:
        self.file_to_poll = path
        self.polling_rate = polling_rate
        self.update_function = None

    def on_update(self, update_func: UpdateFunction) -> UpdateFunction:
        self.update_function = update_func

        return update_func

    def get_modified_time(self) -> bool | float:
        return self.file_to_poll.exists() and self.file_to_poll.stat().st_mtime

    def poll(self) -> NoReturn:
        assert self.update_function is not None

        polling_delay: float = 1 / self.polling_rate

        newest_file_time: float | bool
        remembered_file_time: float | bool = self.get_modified_time()

        while True:
            newest_file_time = self.get_modified_time()

            if newest_file_time != remembered_file_time:
                self.update_function()

                remembered_file_time = newest_file_time

            time.sleep(polling_delay)
