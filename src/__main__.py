import asyncio

from .commands import ShinyHelperCommand


async def main() -> None:
    await ShinyHelperCommand().run()


asyncio.get_event_loop().run_until_complete(main())
