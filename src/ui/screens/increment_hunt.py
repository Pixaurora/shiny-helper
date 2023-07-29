from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label

from ...files import FilePoller, Hunt


class IncrementHuntScreen(Screen):
    hunt: Hunt

    def __init__(self, hunt: Hunt) -> None:
        super().__init__()

        self.hunt = hunt

        poller: FilePoller = self.hunt.create_poller(update_function=self.increment)
        self.set_interval(poller.polling_delay, poller.poll_once)

    @property
    def button_text(self) -> str:
        return f'Encounter! {self.hunt.count}'

    def compose(self) -> ComposeResult:
        yield Label('Gone hunting!')
        yield Button(self.button_text, id='hunt_count')

    async def increment(self) -> None:
        self.hunt.count += 1
        self.hunt.save()

        count_button: Widget = self.get_child_by_id('hunt_count')
        assert isinstance(count_button, Button)

        count_button.label = self.button_text

    async def on_button_pressed(self) -> None:
        await self.increment()
