import discord
from discord.ext import commands
from discord import app_commands
from checks.owner_check import is_owner

TEST_GUILD = discord.Object(364335676549890048)

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def sync(self, interaction:discord.Interaction):
        self.bot.tree.copy_global_to(guild=TEST_GUILD)
        await self.bot.tree.sync(guild=TEST_GUILD)
        await interaction.response.send_message("Commands synced!")
    
async def setup(bot):
    await bot.add_cog(Sync(bot))