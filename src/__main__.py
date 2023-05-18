import asyncio

from .commands import ShinyHelper


async def main() -> None:
    await ShinyHelper().run()


asyncio.get_event_loop().run_until_complete(main())
