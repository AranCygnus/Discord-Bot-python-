from __future__ import annotations

import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime
import pytz


from config import Join_channel_id, Leave_channel_id, Under_line
from core import Bot, Embed
from .. import Plugin

class Event(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """成員加入"""
        channel = self.bot.get_channel(Join_channel_id)
        utc_plus_8 = pytz.timezone('Asia/Taipei')

        embed = Embed(title= "Join!", timestamp= datetime.now(utc_plus_8))
        embed.set_thumbnail(url= member.display_avatar)
        embed.add_field(name= "Welcome!", value= f"【 {member.mention} 】 Join!")
        embed.set_image(url= Under_line)
        embed.set_footer(text= "Made by AranCygnus")

        await channel.send(embed= embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """成員離開"""
        channel = self.bot.get_channel(Leave_channel_id)
        utc_plus_8 = pytz.timezone('Asia/Taipei')

        embed = Embed(title= "Leave!", timestamp= datetime.now(utc_plus_8))
        embed.set_thumbnail(url= member.display_avatar)
        embed.add_field(name= "Bye!", value= f"【 {member.mention} 】 Leave!")
        embed.set_image(url= Under_line)
        embed.set_footer(text= "Made by AranCygnus")

        await channel.send(embed= embed)


    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):

        if msg.author.bot:
            return

        channel_list = [965813058654044220,
                        965819373258428427,
                        1003561050085523496,
                        1003560709415780443,
                        1003560598409314304]
        if msg.channel.id in channel_list:
            if "http" in msg.content:
                pass
            elif len(msg.content) > 200:
                await msg.delete()
                await msg.channel.send(f"都說過不要說這麼多\n{msg.author.mention} 講這麼多話想死484!?")


async def setup(bot: Bot):
    await bot.add_cog(Event(bot))