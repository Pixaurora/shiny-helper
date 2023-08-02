from PIL import Image
from textual.app import ComposeResult
from textual.color import Color
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label
from textual_canvas.canvas import Canvas

from ...files import FilePoller, Hunt


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
        yield Label('Gone hunting!')
        yield Button(self.button_text, id='hunt_count')

        for sprite_type in self.sprites:
            image: Image.Image = self.sprites[sprite_type]
            canvas: Canvas = Canvas(image.width, image.height, id=sprite_type)

            for x in range(image.width):
                for y in range(image.height):
                    color: tuple[int, int, int, int] = image.getpixel((x, y))
                    canvas.set_pixel(x, y, Color(*color))

            yield canvas

    async def increment(self) -> None:
        self.hunt.encounters += 1
        self.hunt.save()

        count_button: Widget = self.get_child_by_id('hunt_count')
        assert isinstance(count_button, Button)

        count_button.label = self.button_text

    async def on_button_pressed(self) -> None:
        await self.increment()
