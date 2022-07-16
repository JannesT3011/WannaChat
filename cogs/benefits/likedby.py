"""
SEE WHO LIKED YOU
"""
import discord
from discord import app_commands
from discord.ext import commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View
from checks.voted import is_voter, voted
from checks.registered import is_registered, registered


class LikedBy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #@is_registered()
    #@is_voter()
    @app_commands.command(name="likedby", description="See the users who liked you")
    async def likedby(self, interaction: discord.Interaction):
        if await registered(self.bot, interaction.user) and await voted(self.bot, interaction.user):
            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
            data = data["liked_by"]
            users = [await self.bot.fetch_user(int(user)) for user in data]
            users = [f"{user.name}#{user.discriminator}" for user in users]
            
            return await interaction.response.send_message(embed=discord.Embed(title="You were liked by these users:", description=", ".join(users), color=EMBED_COLOR).set_footer(text="Add one of the users who liked you and start chatting 🙊", icon_url=self.bot.user.display_avatar.url), ephemeral=True)

async def setup(bot):
    await bot.add_cog(LikedBy(bot))