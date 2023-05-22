import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from config import EMBED_COLOR, CONV_STARTER_API_KEY

class ConvStarter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='starter', description="Get a random conversation starter")
    async def starter_command(self, interaction: discord.Interaction):
        headers = {
	        "X-RapidAPI-Key": CONV_STARTER_API_KEY,
	        "X-RapidAPI-Host": "conversation-starters-api.p.rapidapi.com"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            url = "https://conversation-starters-api.p.rapidapi.com/random"
            async with session.get(url) as response:
                if response.status != 200:
                    return await interaction.response.send_message("Oops, sorry! Something went wrong... try again later", ephemeral=True)
                
                data = await response.json()

                return await interaction.response.send_message(embed=discord.Embed(title="Try this starter:", description=data["starter"], color=EMBED_COLOR), ephemeral=True)


async def setup(bot):
    await bot.add_cog(ConvStarter(bot))