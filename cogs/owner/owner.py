import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='users', aliases=["user"])
    async def users(self, ctx):
        """GET THE AMOUNT OF BOT USERS"""
        data = await self.bot.queuedb.find_one({"_id": "queue"})

        return await ctx.author.send(f"We are currently {len(data['queue'])} users")
    
    @commands.is_owner()
    @commands.command(name="servers", aliases=["guilds"])
    async def guilds(self, ctx):
        """GET THE AMOUNT OF BOT GUILDS"""
        return await ctx.author.send(f"Im currenty on {len(self.bot.guilds)} server(s)")
    
    @commands.is_owner()
    @commands.command(name="status")
    async def status(self, ctx, *, game:str):
        """SET THE BOT STATUS"""
        await self.bot.change_presence(activity=discord.Game(name=game))

        return await ctx.author.send(f"Status set to {game}")
    
    @commands.is_owner()
    @commands.command(name="stats")
    async def stats(self, ctx):
        """SHOW USERS AND SERVERS IN ONE MESSAGE"""
        data = await self.bot.queuedb.find_one({"_id": "queue"})

        return await ctx.author.send(embed=discord.Embed(title="Stats", description=f"**Servers:** {len(self.bot.guilds)}\n**Users:** {len(data['queue'])}"))

async def setup(bot):
    await bot.add_cog(Owner(bot))