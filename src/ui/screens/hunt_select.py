from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, OptionList

from ...errors import NoOptionSelected
from ...files import Hunt, get_hunt_names


class HuntChooser(OptionList):
    def __init__(self, id: str | None = None) -> None:
        super().__init__(*get_hunt_names(), name="Choose your hunt!", id=id)

    def get_hunt(self) -> Hunt:
        option_index: int | None = self.highlighted

        if option_index is None:
            raise NoOptionSelected()

        name: str = str(self.get_option_at_index(option_index).prompt)

        return Hunt.loaded_from_name(name)


class HuntSelectScreen(ModalScreen[Hunt]):
    def compose(self) -> ComposeResult:
        yield Label('Choose one of your hunts to get started!')

        yield HuntChooser(id='hunt_chooser')
        yield Button('Go!', id='go')

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'go':
            hunt: Hunt = self.get_child_by_type(HuntChooser).get_hunt()

            self.dismiss(hunt)
