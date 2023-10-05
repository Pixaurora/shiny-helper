from PIL import Image
from textual.app import App, ComposeResult
from textual.widgets import Button, Header

from ..files import Hunt
from ..pokeapi import PokeAPIClient, gen_7_games
from .screens import HuntSelectScreen, IncrementHuntScreen


class ShinyHelperUI(App):
    CSS_PATH = "shiny_helper.css"
    TITLE = 'Shiny Helper'

    def compose(self) -> ComposeResult:
        yield Header(True, name='Shiny Helper')
        yield Button('Select shiny hunt!', id='select_hunt')

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'select_hunt':
            self.push_screen(HuntSelectScreen(), self.start_hunt)

    async def start_hunt(self, hunt: Hunt) -> None:
        async with PokeAPIClient(gen_7_games[0]) as client:
            images: dict[str, Image.Image] = await client.get_sprite_images(hunt.species)

        self.push_screen(IncrementHuntScreen(hunt, images))
