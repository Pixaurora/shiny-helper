from pathlib import Path

PROGRAM_CONFIG: Path = Path.home() / '.config/shiny-helper'
SAVED_HUNTS: Path = PROGRAM_CONFIG / 'counters'

PROGRAM_CACHE: Path = Path.home() / '.cache/shiny-helper'
IMAGE_CACHE: Path = PROGRAM_CACHE / 'images'
POLLED_FILES: Path = PROGRAM_CACHE / 'polled'


def ready_to_be_file(location: Path) -> bool:
    if not location.exists():
        containing_directory: Path = location.parent
        containing_directory.mkdir(parents=True, exist_ok=True)

        return True

    return location.is_file()


def get_name_from_path(location: Path) -> str:
    return location.name.replace(location.suffix, '')


def get_hunt_location(hunt_name: str) -> Path:
    return SAVED_HUNTS / f'{hunt_name}.json'


def get_hunt_names() -> list[str]:
    if not SAVED_HUNTS.exists():
        return []

    return [get_name_from_path(path) for path in SAVED_HUNTS.iterdir() if path.is_file()]
