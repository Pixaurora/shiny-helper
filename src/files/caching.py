from pathlib import Path

from PIL import Image

from ..errors import InvalidLocationType
from .locations import IMAGE_CACHE, ready_to_be_file


def get_image_from_cache(name: str) -> Image.Image | None:
    cached_location: Path = IMAGE_CACHE / name

    if not cached_location.exists():
        return

    return Image.open(cached_location)


def put_image_into_cache(name: str, image: Image.Image) -> None:
    cached_location: Path = IMAGE_CACHE / name

    if not ready_to_be_file(cached_location):
        raise InvalidLocationType(cached_location)

    image.save(cached_location)
