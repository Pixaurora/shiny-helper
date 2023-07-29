from pathlib import Path

from ..errors import InvalidLocationType
from .locations import IMAGE_CACHE, ready_to_be_file


def get_image_from_cache(name: str) -> bytes | None:
    cached_location: Path = IMAGE_CACHE / name

    if not cached_location.exists():
        return

    return open(cached_location, 'rb').read()


def put_image_into_cache(name: str, data: bytes) -> None:
    cached_location: Path = IMAGE_CACHE / name

    if not ready_to_be_file(cached_location):
        raise InvalidLocationType(cached_location)

    with open(cached_location, 'wb') as file:
        file.write(data)
