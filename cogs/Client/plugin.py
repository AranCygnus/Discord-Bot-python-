from __future__ import annotations

import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional
from datetime import datetime
import pytz

from core import Bot, Embed
from .. import Plugin
from config import Guild_id


class Client(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot


    @app_commands.command(name= "ping", description= "Bot 延遲")
    @app_commands.guilds(discord.Object(id= Guild_id))
    @commands.has_permissions(administrator= True)
    async def ping_command(self, interaction: discord.Interaction):
        """Bot 延遲"""

        utc_plus_8 = pytz.timezone('Asia/Taipei')

        embed = Embed(description= f"{round(self.bot.latency*1000)} ms", timestamp= datetime.now(utc_plus_8))
        await interaction.response.send_message(embed= embed, ephemeral= True)


    @app_commands.command(name= "purge", description= "清除訊息")
    @app_commands.guilds(discord.Object(id= Guild_id))
    @commands.has_permissions(administrator= True)
    @app_commands.describe(amount = "清除數量")
    async def purge_command(self, interaction: discord.Interaction, amount: Optional[int]):
        """清除訊息"""
        if not amount: amount = 1
        embed = Embed(description= f"已清除 **{amount}** 則訊息 | **{interaction.channel}**")
        await interaction.channel.purge(limit= amount)
        await interaction.response.send_message(embed= embed, ephemeral= True)




async def setup(bot: Bot):
    await bot.add_cog(Client(bot))