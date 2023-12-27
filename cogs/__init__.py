from __future__ import annotations

from logging import getLogger; log = getLogger(__name__)

from discord.ext import commands

from core import Bot

__all__ = (
    "Plugin",
)



class Plugin(commands.Cog):
    def __init__(self, bot: Bot):
        super().__init__()

    async def cog_load(self):

        log.info(f" Loaded < {self.qualified_name} > cog.")