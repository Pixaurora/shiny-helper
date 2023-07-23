from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label

from ...files import Counter, get_counter_location

button_text = 'Encounter!'


class IncrementHuntScreen(Screen):
    TITLE = ""

    hunt_path: Path | None = None

    def compose(self) -> ComposeResult:
        yield Label('Gone hunting!')
        yield Button(button_text, id='hunt_count')

    async def prepare(self, hunt_name: str) -> None:
        self.hunt_path = get_counter_location(hunt_name)

        await self.update_screen()

    async def update_screen(self) -> None:
        assert self.hunt_path is not None

        count_button: Widget = self.get_child_by_id('hunt_count')
        assert isinstance(count_button, Button)

        with Counter(self.hunt_path) as counter:
            count_button.label = f'{button_text} Count: {counter.count}'

    async def on_button_pressed(self) -> None:
        with Counter(self.hunt_path) as counter:
            counter.count += 1

        await self.update_screen()
