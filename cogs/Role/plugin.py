from __future__ import annotations

import discord
from discord.ext import commands
from discord import app_commands

from core import Bot
from .. import Plugin
from config import Guild_id, Rigel_id

class Button_role(discord.ui.View):
    def __init__(self):
        super().__init__(timeout= None)

    @discord.ui.button(label= "Rigel", style= discord.ButtonStyle.green, custom_id= "role_button")
    async def rigel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(discord.role) is not discord.Role:
            discord.role = interaction.guild.get_role(Rigel_id)
        if discord.role not in interaction.user.roles:
            await interaction.user.add_roles(discord.role)
            await interaction.response.send_message(f"妳獲得了身分組 {discord.role.mention}!", ephemeral= True)
        else:
            await interaction.response.send_message(f"妳已經是 {discord.role.mention}!", ephemeral= True)


class Role(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name= "rigel", description= "領取Rigel身分組")
    @app_commands.guilds(discord.Object(id= Guild_id))
    @commands.has_permissions(administrator= True)
    async def rigel_command(self, interaction: discord.Interaction):
        """領取Rigel身分組"""
        if interaction.guild.id == Guild_id:
            await interaction.response.send_message("領取身分組", view= Button_role())
        else:
            await interaction.response.send_message("這伺服器沒有權限", ephemeral= True)



async def setup(bot: Bot):
    await bot.add_cog(Role(bot))

