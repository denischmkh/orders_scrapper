import asyncio

from bot import run_bot_client
from users import run_users_clients


async def main():
    asyncio.create_task(await run_bot_client())
    asyncio.create_task(await run_users_clients())


if __name__ == '__main__':
    asyncio.run(main())