from ..ui import ShinyHelperUI
from .base import NamedCommand


class UICommand(NamedCommand):
    @property
    def name(self) -> str:
        return 'ui'

    async def main(self) -> None:
        app = ShinyHelperUI()

        try:
            await app.run_async()
        finally:
            self._loop = None
            self._thread_id = 0
