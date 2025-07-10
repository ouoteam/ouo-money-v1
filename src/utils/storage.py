import contextlib
import os

import aiofiles
import orjson


class Storage:
    """
    Storage management class for the bot.
    """

    async def get_guild_data(guild_id: int) -> dict:
        """
        Get guild data from the database.

        :param guild_id: The ID of the guild to get data for.
        :return: The guild data.
        """
        if os.path.exists(f"data/{guild_id}.json"):
            async with aiofiles.open(f"data/{guild_id}.json", "rb") as f:
                with contextlib.suppress(orjson.JSONDecodeError):
                    return orjson.loads(await f.read())
        return {"name": "貨幣", "admin": None, "users": {}}

    async def set_guild_data(guild_id: int, data: dict) -> None:
        """
        Set guild data to the database.

        :param guild_id: The ID of the guild to set data for.
        :param data: The guild data.
        """
        async with aiofiles.open(f"data/{guild_id}.json", "wb") as f:
            await f.write(orjson.dumps(data))
