from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label

from ...files import Counter, FilePoller


class IncrementHuntScreen(Screen):
    TITLE = ""

    hunt: Counter

    def __init__(self, hunt: Counter) -> None:
        super().__init__()

        self.hunt = hunt

        poller: FilePoller = FilePoller(Path('./watched'), 5, self.increment)
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
