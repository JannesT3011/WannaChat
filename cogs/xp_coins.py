import discord
from discord.ext import commands
from discord import app_commands
from checks.registered import is_registered
from config import EMBED_COLOR

class XP_Coins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def create_embed(self, currency: str, data: dict) -> discord.Embed:
        embed = discord.Embed(title=f"You own `{data[currency]}{currency}`", color=EMBED_COLOR if data["color"] == "" else discord.Colour.from_str(data["color"]))
        
        return embed

    @app_commands.command(name="coins", description="See your owned coins")
    @is_registered()
    async def coins(self, interaction: discord.Interaction):
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        
        return await interaction.response.send_message(embed=self.create_embed("coins", data))
    
    @app_commands.command(name="xp", description="See your owned XP")
    @is_registered()
    async def xp(self, interaction: discord.Interaction):
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        
        return await interaction.response.send_message(embed=self.create_embed("xp", data))

async def setup(bot):
    await bot.add_cog(XP_Coins(bot))