from textual.app import App, ComposeResult
from textual.widgets import Button, Header

from ..files import Hunt
from .screens import HuntSelectScreen, IncrementHuntScreen


class ShinyHelperUI(App):
    TITLE = 'Shiny Helper'

    def compose(self) -> ComposeResult:
        yield Header(True, name='Shiny Helper')
        yield Button('Select shiny hunt!', id='select_hunt')

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'select_hunt':
            self.push_screen(HuntSelectScreen(), self.start_hunt)

    def start_hunt(self, hunt: Hunt):
        self.push_screen(IncrementHuntScreen(hunt))
