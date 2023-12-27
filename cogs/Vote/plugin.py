from __future__ import annotations

import discord
from discord.ext import commands
from discord import app_commands

import re

from core import Bot, Embed
from .. import Plugin
from config import Guild_id, Under_line

class Vote(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]


    @app_commands.command(name= "poll", description= "建立投票")
    @app_commands.guilds(discord.Object(id= Guild_id))
    @commands.has_permissions(administrator= False)
    async def poll_command(self, interaction: discord.Interaction, question: str, options1: str, options2: str, options3: str= None, options4: str= None, options5: str= None):
        """建立投票"""
        await interaction.response.send_message("建立投票中", ephemeral= True)
        try:
            listen = [options1, options2, options3, options4, options5]
            your_list = []
            for i in listen:
                if i != None:
                    your_list.append(i)

            if len(your_list) == 2:
                embed = Embed(title= f"{question}")
                embed.add_field(name= f"1️⃣ | {options1}", value= " ", inline= False)
                embed.add_field(name= f"2️⃣ | {options2}", value= " ", inline= False)

                embed.set_image(url= Under_line)
                embed.set_footer(text= "Made by AranCygnus")

                message = await interaction.channel.send(embed= embed)
                await message.add_reaction("1️⃣")
                await message.add_reaction("2️⃣")

            elif len(your_list) == 3:
                embed = Embed(title= f"{question}")
                embed.add_field(name= f"1️⃣ | {options1}", value= " ", inline= False)
                embed.add_field(name= f"2️⃣ | {options2}", value= " ", inline= False)
                embed.add_field(name= f"3️⃣ | {options3}", value= " ", inline= False)

                embed.set_image(url= Under_line)
                embed.set_footer(text= "Made by AranCygnus")

                message = await interaction.channel.send(embed= embed)
                await message.add_reaction("1️⃣")
                await message.add_reaction("2️⃣")
                await message.add_reaction("3️⃣")

            elif len(your_list) == 4:
                embed = Embed(title= f"{question}")
                embed.add_field(name= f"1️⃣ | {options1}", value= " ", inline= False)
                embed.add_field(name= f"2️⃣ | {options2}", value= " ", inline= False)
                embed.add_field(name= f"3️⃣ | {options4}", value= " ", inline= False)
                embed.add_field(name= f"4️⃣ | {options5}", value= " ", inline= False)

                embed.set_image(url= Under_line)
                embed.set_footer(text= "Made by AranCygnus")

                message = await interaction.channel.send(embed= embed)
                await message.add_reaction("1️⃣")
                await message.add_reaction("2️⃣")
                await message.add_reaction("3️⃣")
                await message.add_reaction("4️⃣")

            elif len(your_list) == 5:
                embed = Embed(title= f"{question}")
                embed.add_field(name= f"1️⃣ | {options1}", value= " ", inline= False)
                embed.add_field(name= f"2️⃣ | {options2}", value= " ", inline= False)
                embed.add_field(name= f"3️⃣ | {options3}", value= " ", inline= False)
                embed.add_field(name= f"4️⃣ | {options4}", value= " ", inline= False)
                embed.add_field(name= f"5️⃣ | {options5}", value= " ", inline= False)

                embed.set_image(url= Under_line)
                embed.set_footer(text= "Made by AranCygnus")

                message = await interaction.channel.send(embed= embed)
                await message.add_reaction("1️⃣")
                await message.add_reaction("2️⃣")
                await message.add_reaction("3️⃣")
                await message.add_reaction("4️⃣")
                await message.add_reaction("5️⃣")
            await interaction.edit_original_response(content= "建立成功")

        except Exception as e:
            print(e)
            await interaction.delete_original_response()
            await interaction.followup.send("⚠️Error", ephemeral= True)


async def setup(bot: Bot):
    await bot.add_cog(Vote(bot))