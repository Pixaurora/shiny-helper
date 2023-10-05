from __future__ import annotations

from PIL import Image
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label, Static

from ...files import FilePoller, Hunt
from ..common import ImageCanvas


class HuntVisualizer(Static):
    parent_screen: IncrementHuntScreen

    def __init__(self, parent: IncrementHuntScreen) -> None:
        super().__init__(id='hunt_visualizer')

        self.parent_screen = parent

    def compose(self) -> ComposeResult:
        for form, sprite in self.parent_screen.sprites.items():
            yield ImageCanvas(sprite, id=form)

    async def on_button_pressed(self) -> None:
        await self.parent_screen.increment()


class IncrementHuntScreen(Screen):
    hunt: Hunt
    sprites: dict[str, Image.Image]

    def __init__(self, hunt: Hunt, sprites: dict[str, Image.Image]) -> None:
        super().__init__()

        self.hunt = hunt
        self.sprites = sprites

        poller: FilePoller = self.hunt.create_poller(update_function=self.increment)
        self.set_interval(poller.polling_delay, poller.poll_once)

    @property
    def button_text(self) -> str:
        return f'Encounter! {self.hunt.encounters}'

    def compose(self) -> ComposeResult:
        yield Container(Label('Gone hunting!'), Button(self.button_text, id='hunt_count'), HuntVisualizer(self))

    async def increment(self) -> None:
        self.hunt.encounters += 1
        self.hunt.save()

        count_button: Widget = self.get_child_by_id('hunt_count')
        assert isinstance(count_button, Button)

        count_button.label = self.button_text

    async def on_button_pressed(self) -> None:
        await self.increment()
