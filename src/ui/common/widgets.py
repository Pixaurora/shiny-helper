from PIL import Image
from textual.color import Color
from textual_canvas import Canvas


class ImageCanvas(Canvas):
    def __init__(self, image: Image.Image, id: str | None = None) -> None:
        super().__init__(image.width, image.height, id=id)

        for x in range(image.width):
            for y in range(image.height):
                color: tuple[int, int, int, int] = image.getpixel((x, y))
                self.set_pixel(x, y, Color(*color))
