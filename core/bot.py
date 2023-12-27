from __future__ import annotations

from typing import Optional
import os
import aiosqlite

from .embed import Embed
from config import Guild_id, DB_NAME, PASSWORD, PORT, USER, HOST

from logging import getLogger; log = getLogger("Bot")

from discord.ext import commands
import discord

__all__ = (
    "Bot",
)

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix= "!",
            intents= discord.Intents.all(),
            chunk_guild_at_startup = False
        )
        self.synced = False
        self.anti_spam = commands.CooldownMapping.from_cooldown(10, 10, commands.BucketType.member)


    async def setup_hook(self):
        log.info("Running setup...")

        for file in os.listdir("cogs"):
            if not file.startswith("__"):
                await self.load_extension(f"cogs.{file}.plugin")

    async def on_ready(self):

        game = discord.Game("難道你良心不會痛嗎?")
        await self.change_presence(status= discord.Status.online, activity= game)

        await self.wait_until_ready()
        if not self.synced:
            sync_commands = await self.tree.sync(guild = discord.Object(id= Guild_id))
            self.synced = True
            log.info(f"Successfully synced {len(sync_commands)} commands.")


        setattr(Bot, "db", await aiosqlite.connect("databases/level.db"))
        async with Bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")

        log.info(f"Logged in as {self.user} (ID: {self.user.id})")
        log.info("Bot ready.")


    async def on_connected(self):
        log.info(f"Connected to Discord (latency: {self.latency * 1000:,.0f} ms).")


    async def on_message(self, msg: discord.Message):
        if type(msg.channel) is not discord.TextChannel or msg.author.bot: return
        if not msg.author.bot:
            await self.process_commands(msg)

        bucket = self.anti_spam.get_bucket(msg)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await msg.channel.send(f"馬的智障{msg.author.mention}\n不要洗頻!!!")



    async def success(
                        self,
                        message: str,
                        interaction: discord.Interaction,
                        *,
                        ephemeral: bool = False,
                        embed: Optional[bool] = True
                        ) -> Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed= Embed(description= message, color= discord.Colour.green(),
                    ephemeral= ephemeral)
                )
            return await interaction.response.send_message(
                embed= Embed(description= message, color= discord.Colour.green()),
                ephemeral= ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content= f"✔️ | {message}", ephemeral= ephemeral)
            return await interaction.response.send_message(content= f"✔️ | {message}", ephemeral= ephemeral)

    async def error(
                        self,
                        message: str,
                        interaction: discord.Interaction,
                        *,
                        ephemeral: bool = False,
                        embed: Optional[bool] = True
                        ) -> Optional[discord.WebhookMessage]:
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(
                    embed= Embed(description= message, color= discord.Colour.red(),
                    ephemeral= ephemeral)
                )
            return await interaction.response.send_message(
                embed= Embed(description= message, color= discord.Colour.red()),
                ephemeral= ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content= f"❌ | {message}", ephemeral= ephemeral)
            return await interaction.response.send_message(content= f"❌ | {message}", ephemeral= ephemeral)