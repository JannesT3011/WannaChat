import discord
from discord.ext import commands
from database.database import Database

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='login')
    async def login(self, ctx):
        try:
            await Database().init_db(str(ctx.author.id))
        except:
            return await ctx.author.send("Already login!", delete_after=4)
        await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(ctx.author.id)}})
        return await ctx.author.send("Login successful!")
    
    @commands.command(name="logoff")
    async def logoff(self, ctx):
        try:
            await Database().delete_db(str(ctx.author.id))
        except:
            return await ctx.send("Already logoff!", delete_after=4)
        await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(ctx.author.id)}})
        return await ctx.author.send("Logoff successful!")

def setup(bot):
    bot.add_cog(Login(bot))