import discord
from discord.ext import commands
from discord import app_commands
from checks.base_check import is_owner

TEST_GUILD = discord.Object(364335676549890048)

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Sync all commands!")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def sync(self, interaction:discord.Interaction):
        await self.bot.tree.sync()
        await interaction.response.send_message("Commands synced!")
    
    @commands.is_owner()
    @commands.command(name="sync")
    async def _sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Commands synced!")
    
async def setup(bot):
    await bot.add_cog(Sync(bot), guild=bot.test_guild)