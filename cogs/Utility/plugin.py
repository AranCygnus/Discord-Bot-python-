from __future__ import annotations

from typing import Optional
import pytz
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

from core import Bot, Embed
from .. import Plugin
from config import Guild_id, Under_line, Version

class Utility(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot


    @app_commands.command(name= "bot_info", description= "機器人資訊")
    @app_commands.guilds(discord.Object(id= Guild_id))
    async def info(self, interaction: discord.Interaction):
        """機器人資訊"""
        utc_plus_8 = pytz.timezone('Asia/Taipei')

        embed = Embed(title= "About ツッコミBot", timestamp= datetime.now(utc_plus_8))
        embed.set_thumbnail(url= "https://i.imgur.com/Vedlve0.jpeg")
        embed.add_field(name= "Developers", value= "`AranCygnus` (<@773741735305019442>)", inline= False)
        embed.add_field(name= "Version", value= Version, inline= True)
        embed.add_field(name= "Powered by", value= "`discord.py v{}`".format(discord.__version__), inline= True)
        embed.add_field(name= "Prefix", value= "`!`", inline= False)
        embed.set_footer(text= "Made by AranCygnus")
        embed.set_image(url= Under_line)

        await interaction.response.send_message(embed= embed)


    @app_commands.command(name= "member_info", description= "使用者資訊")
    @app_commands.guilds(discord.Object(id= Guild_id))
    @app_commands.describe(target= "選擇一個成員")
    async def member_info(self, interaction: discord.Interaction, target: Optional[discord.Member]):
        """使用者資訊"""

        utc_plus_8 = pytz.timezone('Asia/Taipei')


        embed = Embed(title="User Information", timestamp= datetime.now(utc_plus_8))
        embed.set_author(name= str(target), icon_url= target.display_avatar)
        embed.set_thumbnail(url= target.display_avatar)
        embed.add_field(name= "Name", value= target.name, inline= True)
        embed.add_field(name= "Nickname", value= target.nick if target.nick else "N/A", inline= True)
        embed.add_field(name= "Top role", value= target.top_role.mention, inline= False)
        embed.add_field(name= "Created on", value= target.created_at.strftime("%Y/%m/%d"), inline= True)
        embed.add_field(name= "Joined on", value= target.joined_at.strftime("%Y/%m/%d"), inline= True)
        embed.set_footer(text= "Made by AranCygnus")
        embed.set_image(url= Under_line)

        await interaction.response.send_message(embed= embed)




async def setup(bot: Bot):
    await bot.add_cog(Utility(bot))