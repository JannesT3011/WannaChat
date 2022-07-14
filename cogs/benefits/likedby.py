"""
SEE WHO LIKED YOU
"""
import discord
from discord.ext import commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View
from checks.voted import is_voter
from checks.registered import is_registered


class LikedBy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @is_registered()
    @is_voter()
    @commands.command(name="likedby") # TODO random button!
    async def likedby(self, ctx):
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        data = data["liked_by"]
        users = [await self.bot.fetch_user(int(user)) for user in data]
        users = [f"{user.name}#{user.discriminator}" for user in users]
        
        return await ctx.author.send(embed=discord.Embed(title="You were liked by these users:", description=", ".join(users), color=EMBED_COLOR).set_footer(text="Add one of the users who liked you and start chatting 🙊", icon_url=self.bot.user.display_avatar.url))

async def setup(bot):
    await bot.add_cog(LikedBy(bot))