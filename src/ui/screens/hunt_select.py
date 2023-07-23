from textual.app import App, ComposeResult, DOMNode
from textual.screen import Screen
from textual.widgets import Button, Label, OptionList

from ...files import get_counter_names
from .increment_hunt import IncrementHuntScreen


class HuntSelectScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label('Choose one of your hunts to get started!')

        yield OptionList(*get_counter_names())
        yield Button('Go!')

    async def on_button_pressed(self) -> None:
        options: OptionList = self.get_child_by_type(OptionList)
        option_index: int = options.highlighted or 0

        hunt_name: str = str(options.get_option_at_index(option_index).prompt)

        app: DOMNode | None = self.parent
        assert isinstance(app, App)

        await app.push_screen('increment_hunt')

        screen: Screen = app.screen
        assert isinstance(screen, IncrementHuntScreen)

        await screen.prepare(str(hunt_name))
