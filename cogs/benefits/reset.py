"""RESET DISLIKED USERS

ALSO RESET LIKED USERS
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View
from checks.voted import is_voter
from checks import is_voter, is_registered

class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reset_group = app_commands.Group(name="reset", description="Reset your likes or dislikes")

    @reset_group.command(name="all", description="Reset likes and dislikes")
    @is_registered()
    @is_voter()
    @app_commands.checks.cooldown(1, 180.0, key=lambda i: (i.guild_id, i.user.id))
    async def reset(self, interaction: discord.Interaction):
        """RESET YOUR LIKES AND DISLIKES"""
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

    @reset_group.command(name="likes", description="Reset your likes")
    @is_registered()
    @is_voter()
    @app_commands.checks.cooldown(1, 180.0, key=lambda i: (i.guild_id, i.user.id))
    async def reset_likes(self, interaction: discord.Interaction):
        """RESET YOUR LIKES"""
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

    @is_registered()
    @is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @reset_group.command(name="dislikes", description="Reset your dislikes")
    async def reset_dislikes(self, interaction: discord.Interaction):
        """RESET YOUR DISLIKES"""
        async def confirm_button_interaction(interaction):
            await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"disliked_users": []}})
            return await interaction.response.send_message(embed=discord.Embed(title="Successfully reseted your disliked users!", color=EMBED_COLOR), ephemeral=True)
        
        async def cancel_button_interaction(interaction):
            await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)
        
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