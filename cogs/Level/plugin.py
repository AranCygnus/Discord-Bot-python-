from __future__ import annotations


import discord
from discord.ext import commands
from discord import app_commands

import random
from easy_pil import *
import pytz
from datetime import datetime

from core import Bot, Embed
from .. import Plugin
from config import Guild_id, Bot_channel, Under_line



class Level(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):

        if msg.author.bot:
            return

        author = msg.author
        guild = msg.guild
        async with Bot.db.cursor() as cursor:

            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id))
            xp = await cursor.fetchone()

            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id))
            level = await cursor.fetchone()

            if not xp or level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id))
                await Bot.db.commit()

            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            if level < 5:
                xp += random.randint(5, 10)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id))
            else:
                rand = random.randint(1, (level // 4))
                if rand == 1:
                    xp += random.randint(5, 10)
                    await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id))
            if xp >= 100:
                level += 1
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id))
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id))

                channel = self.bot.get_channel(Bot_channel)
                utc_plus_8 = pytz.timezone('Asia/Taipei')

                embed = Embed(title= "Level up!", description= f"{author.mention} has leveled up to level **{level}** !", timestamp= datetime.now(utc_plus_8))

                embed.set_footer(text= "Made by AranCygnus")
                embed.set_image(url= Under_line)
                await channel.send(embed= embed)

        await Bot.db.commit()


    @app_commands.command(name= "level", description= "查看等級")
    @app_commands.guilds(discord.Object(id= Guild_id))
    @commands.has_permissions(administrator= True)
    async def level_command(self, interaction: discord.Interaction, member: discord.Member):
        """查看等級"""
        async with Bot.db.cursor() as cursor:

            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, member.guild.id))
            xp = await cursor.fetchone()

            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, member.guild.id))
            level = await cursor.fetchone()

            if not xp or level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, member.guild.id))
                await Bot.db.commit()

            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 0
                level = 0

            user_data = {
                "name": f"{member.name}",
                "xp": xp,
                "level": level,
                "next_level_xp": 100,
                "percentage": xp,
            }

            background = Editor(Canvas((900, 300), color= "#141414"))
            profile_picture = await load_image_async(str(member.avatar.url))
            profile = Editor(profile_picture).resize((150, 150)).circle_image()

            poppins = Font.poppins(size= 48)
            poppins_small = Font.poppins(size= 30)

            card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

            background.polygon(card_right_shape, color= "#FFFFFF")
            background.paste(profile, (30, 30))

            background.rectangle((30, 220), width= 650, height= 40, color= "#FFFFFF")
            background.bar((30, 220), max_width=650, height= 40, percentage= user_data["percentage"], color= "#282828", radius= 20)
            background.text((200, 40), user_data["name"], font= poppins, color= "#FFFFFF")

            background.rectangle((200, 100), width= 350, height= 2, fill= "#FFFFFF")
            background.text((200, 130), f"Level - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level_xp']}", font= poppins_small, color= "#FFFFFF")

            file = discord.File(fp= background.image_bytes, filename= "level_card.png")
            await interaction.channel.send(file= file)

async def setup(bot: Bot):
    await bot.add_cog(Level(bot))

