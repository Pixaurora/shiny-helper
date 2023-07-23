from textual.app import App, ComposeResult
from textual.widgets import Header

from .screens import HuntSelectScreen, IncrementHuntScreen


class ShinyHelperUI(App):
    TITLE = 'Shiny Helper'

    SCREENS = {'increment_hunt': IncrementHuntScreen(), 'hunt_select': HuntSelectScreen()}

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(True, name='Shiny Helper')

        self.push_screen('hunt_select')
