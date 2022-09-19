"""SET A PROFILE GIVE
TODO: DB UPDATE GIF FIELD DONE! (name gif, if not null).
embed.set_image()
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import EMBED_COLOR
from checks import is_registered, is_voter

class Gif(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="gif", description="Set a profile GIF") # TODO reset gif
    @app_commands.describe(gif="The giphy.com gif you want to add to your profile")
    @is_registered()
    #@is_voter()
    async def gif(self, interaction: discord.Interaction, gif: str):
        if not gif.startswith("https://media.giphy.com"):
            return await interaction.response.send_message("Please use a giphy GIF!", ephemeral=True)
        if not gif.endswith("/giphy.gif"):
            return await interaction.response.send_message("Please copy the Giphy link that ends with `/giphy.gif`!", ephemeral=True)

        r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"gif": gif}})       
        await interaction.response.defer(ephemeral=True, thinking=True)

        if r:
            return await interaction.followup.send(embed=discord.Embed(title="Profile GIF set successfully!", color=EMBED_COLOR).set_image(url=gif), ephemeral=True)

    #@app_commands.command(name="color", description="Set your profile color")
    #@is_registered()
    #@is_voter()
    #async def profile_color(self, interaction: discord.Interaction, color: str):
    #    if not is_color_like(color) and not color.startswith("#"):
    #        return await interaction.response.send_message("please provide a valid color!", ephemeral=True)
    #    r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"color": color}})
    #    
    #    await interaction.response.defer(ephemeral=True, thinking=True)
    #    if r:
    #        return await interaction.followup.send(embed=discord.Embed(title=f"Profile color set to: {color}"))

    
async def setup(bot):
    await bot.add_cog(Gif(bot))