"""SET A PROFILE GIVE
TODO: DB UPDATE GIF FIELD DONE! (name gif, if not null).
embed.set_image()
"""

import discord
from discord.ext import commands
from discord import app_commands
from config import EMBED_COLOR
from checks import is_registered, is_premium
from matplotlib.colors import is_color_like

class Gif(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="gif", description="Set a profile GIF") # TODO reset gif
    @app_commands.describe(gif="The giphy.com gif you want to add to your profile")
    @is_registered()
    @is_premium()
    async def gif(self, interaction: discord.Interaction, gif: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        if not gif.startswith("https://media.giphy.com"):
            return await interaction.followup.send("Please use a giphy GIF!", ephemeral=True)
        if not gif.endswith("/giphy.gif"):
            return await interaction.followup.send("Please copy the Giphy link that ends with `/giphy.gif`!", ephemeral=True)

        r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"gif": gif}})       

        if r:
            return await interaction.followup.send(embed=discord.Embed(title="Profile GIF set successfully!", color=EMBED_COLOR).set_image(url=gif), ephemeral=True)

    @app_commands.command(name="color", description="Set your profile color")
    @is_registered()
    @is_premium()
    async def color(self, interaction: discord.Interaction, color: str):
        await interaction.response.defer(ephemeral=True, thinking=True)

        if not is_color_like(color) and not color.startswith("#"):
            return await interaction.followup.send("Please provide a valid color!", ephemeral=True)
        r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"color": color}})
        
        if r:
            return await interaction.followup.send(embed=discord.Embed(title=f"Profile color set to: {color}"))

    song_group = app_commands.Group(name="song", description="Add/Remove a spotify song to your profile")

    @song_group.command(name="add", description="Set your profile color")
    @is_registered()
    @is_premium()
    async def song_add(self, interaction: discord.Interaction, song:str):
        await interaction.response.defer(ephemeral=True, thinking=True)

        if not song.startswith("https://open.spotify.com"):
            return interaction.followup.send("Please use a spotify song!", ephemeral=True)
        
        await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"song": song}})

        return await interaction.followup.send(embed=discord.Embed(title="Song successfully set!", url=song))

    @song_group.command(name="remove", description="Set your profile color")
    @is_registered()
    @is_premium()
    async def song_remove(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"song": None}})

        return await interaction.followup.send(embed=discord.Embed(title="Song removed!"))

async def setup(bot):
    await bot.add_cog(Gif(bot))