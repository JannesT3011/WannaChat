"""RESET DISLIKED USERS

ALSO RESET LIKED USERS
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View
from checks.voted import is_voter, voted
from checks.registered import is_registered, registered

class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reset_group = app_commands.Group(name="reset", description="Reset your likes or dislikes")

    #@is_registered()
    #@is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @reset_group.command(name="all", description="Reset likes and dislikes")
    async def reset(self, interaction: discord.Interaction):
        """RESET YOUR LIKES AND DISLIKES"""
        if await registered(self.bot, interaction.user) and await voted(self.bot, interaction.user):
            async def confirm_button_interaction(interaction):
                await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"disliked_users": []}})
                await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"liked_users": []}})

                return await interaction.response.send_message(embed=discord.Embed(title="Successfully reseted your liked and disliked users!", color=EMBED_COLOR), ephemeral=True)

            async def cancel_button_interaction(interaction):
                await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)

            confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
            cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
            confirm_button.callback = confirm_button_interaction
            cancel_button.callback = cancel_button_interaction
            view = View()
            view.add_item(confirm_button)
            view.add_item(cancel_button)

            await interaction.response.send_message(embed=discord.Embed(title="Are you sure you want to reset your liked and disliked users?", color=EMBED_COLOR), view=view, ephemeral=True)

    #@is_registered()
    #@is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @reset_group.command(name="likes", description="Reset your likes")
    async def reset_likes(self, interaction: discord.Interaction):
        """RESET YOUR LIKES"""
        if await registered(self.bot, interaction.user) and await voted(self.bot, interaction.user):
            async def confirm_button_interaction(interaction):
                await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"liked_users": []}})
                return await interaction.response.send_message(embed=discord.Embed(title="Successfully reseted your liked users!", color=EMBED_COLOR), ephemeral=True)
            
            async def cancel_button_interaction(interaction):
                await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)

            confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
            cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
            confirm_button.callback = confirm_button_interaction
            cancel_button.callback = cancel_button_interaction
            view = View()
            view.add_item(confirm_button)
            view.add_item(cancel_button)

            await interaction.response.send_message(embed=discord.Embed(title="Are you sure you want to reset your liked users?", color=EMBED_COLOR), view=view, ephemeral=True)

    #@is_registered()
    #@is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @reset_group.command(name="dislikes", description="Reset your dislikes")
    async def reset_dislikes(self, interaction: discord.Interaction):
        """RESET YOUR DISLIKES"""
        if await registered(self.bot, interaction.user) and await voted(self.bot, interaction.user):
            async def confirm_button_interaction(interaction):
                await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"disliked_users": []}})
                return await interaction.response.send_message(embed=discord.Embed(title="Successfully reseted your disliked users!", color=EMBED_COLOR), ephemeral=True)
            
            async def cancel_button_interaction(interaction):
                await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None, ephemeral=True)

            confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
            cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
            confirm_button.callback = confirm_button_interaction
            cancel_button.callback = cancel_button_interaction
            view = View()
            view.add_item(confirm_button)
            view.add_item(cancel_button)

            await interaction.response.send_message(embed=discord.Embed(title="Are you sure you want to reset your disliked users?", color=EMBED_COLOR), view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Reset(bot))