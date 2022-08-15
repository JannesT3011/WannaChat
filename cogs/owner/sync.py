import discord
from discord.ext import commands
from discord import app_commands

def is_owner(interaction:discord.Interaction):
    return interaction.user.id == 311450463553847299

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.check(is_owner)
    async def sync(self, interaction:discord.Interaction):
        self.bot.tree.copy_global_to(guild=discord.Object(id=364335676549890048))
        await self.bot.tree.sync(guild=discord.Object(id=364335676549890048))
        await interaction.response.send_message("Done!")
    
async def setup(bot):
    await bot.add_cog(Sync(bot))