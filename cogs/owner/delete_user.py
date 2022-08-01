"""DELETE USER wc.userdel user"""
import discord
from discord.ext import commands
from database.database import Database

class DelUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='deluser')
    async def deluser(self, ctx, *, id:int):
        try:
            await Database().delete_db(str(id))
            await self.bot.queuedb.update_many({"_id": "queue"}, {"$pull": {"queue": str(id)}})
        except:
            return await ctx.send("Cant find this user")

        return await ctx.send(f"User {id} deleted!")

async def setup(bot):
    await bot.add_cog(DelUser(bot))