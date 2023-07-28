from ..ui import ShinyHelperUI
from .base import NamedCommand


class UICommand(NamedCommand):
    @property
    def name(self) -> str:
        return 'ui'

    async def main(self) -> None:
        app = ShinyHelperUI()

        await app.run_async()
