"""
SEE WHO LIKED YOU
"""
import discord
from discord import app_commands
from discord.ext import commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View
from checks import is_voter, is_registered


class LikedBy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="likedby", description="See the users who liked you")
    @is_registered()
    @is_voter()
    async def likedby(self, interaction: discord.Interaction):
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        data = data["liked_by"]
        users = [await self.bot.fetch_user(int(user)) for user in data]
        users = [f"`{user.name}#{user.discriminator}`" for user in users]
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if data:
            return await interaction.followup.send(embed=discord.Embed(title="You were liked by these users:", description=", ".join(users), color=EMBED_COLOR).set_footer(text="Add one of the users who liked you and start chatting 🙊", icon_url=self.bot.user.display_avatar.url), ephemeral=True)

async def setup(bot):
    await bot.add_cog(LikedBy(bot))