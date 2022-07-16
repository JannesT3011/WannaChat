import discord
from discord.ext import commands
from database.database import Database
from config import EMBED_COLOR, PREFIX
from discord.ui import Button, View
from discord import app_commands

from cogs.profile import SelectView

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="login", description="Register your account")
    async def login(self, interaction:discord.Interaction):
        """LOGIN/CREATE YOUR ACCOUNT"""
        try:
            await Database().init_db(str(interaction.user.id))
        except:
            return await interaction.response.send_message(embed=discord.Embed(title="Already login!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infos\nStart by selecting your gender:"), view=SelectView(author=interaction.user, bot=self.bot), ephemeral=True)
        await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(interaction.user.id)}})

        return await interaction.response.send_message(embed=discord.Embed(title="Login successful!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infos\nStart by selecting your gender:", color=EMBED_COLOR), view=SelectView(author=interaction.user, bot=self.bot), ephemeral=True)
    
    @app_commands.command(name="logoff", description="Delete your account")
    async def logoff(self, interaction:discord.Interaction):
        """LOGOFF/DELETE YOUR ACCOUNT"""
        async def logoff_confirm_button(interaction):
            try:
                await Database().delete_db(str(interaction.user.id))
            except:
                await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)
                return await interaction.user.send("Already logoff!")
            await self.bot.queuedb.update_many({"_id": "queue"}, {"$pull": {"queue": str(interaction.user.id)}})

            return await interaction.response.edit_message(embed=discord.Embed(title="Logoff successful!", color=EMBED_COLOR).set_footer(text=f"Use `{PREFIX}help` to get more infos"), view=None)

        async def logoff_cancel_button(interaction):
            await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)

        confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
        confirm_button.callback = logoff_confirm_button
        cancel_button.callback = logoff_cancel_button
        view = View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)
        
        await interaction.response.send_message(embed=discord.Embed(title="Are you sure you want to delete your account?", color=EMBED_COLOR), view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Login(bot))