from PIL import Image

SPRITE_MAPPING = {'normal': 'front_default', 'shiny': 'front_shiny'}


def prepare_sprite(sprite: Image.Image) -> Image.Image:
    sprite = sprite.convert('RGBA')

    for x in range(sprite.width):
        for y in range(sprite.height):
            coordinate: tuple[int, int] = (x, y)

            if sprite.getpixel(coordinate)[3] == 0:
                sprite.putpixel(coordinate, (0, 0, 0, 0))

    return sprite.crop(sprite.getbbox())
