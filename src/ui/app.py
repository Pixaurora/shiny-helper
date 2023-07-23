from textual.app import App, ComposeResult
from textual.widgets import Header

from .screens import HuntSelectScreen


class ShinyHelperUI(App):
    TITLE = 'Shiny Helper'

    def compose(self) -> ComposeResult:
        yield Header(True, name='Shiny Helper')

        self.push_screen(HuntSelectScreen())
