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
    async def status(self, ctx, type:str, *, game:str):
        """SET THE BOT STATUS"""
        if type == "game":
            await self.bot.change_presence(activity=discord.Game(name=game))
        elif type == "watching":
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=game))
        elif type == "listening":
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=game))
        else:
            return await ctx.author.send("No valid type -> `game, watching, listening`")

        return await ctx.author.send(f"Status set to {game}")
    
    @commands.is_owner()
    @commands.command(name="stats")
    async def stats(self, ctx):
        """SHOW USERS AND SERVERS IN ONE MESSAGE"""
        data = await self.bot.queuedb.find_one({"_id": "queue"})
        gc_data = await self.bot.gcserversdb.find_one({"_id": "servers"})

        return await ctx.author.send(embed=discord.Embed(title="Stats", description=f"**Servers:** {len(self.bot.guilds)}\n**Users:** {len(data['queue'])}\n**GC Channels:**{len(gc_data['channels'])}", timestamp=ctx.message.created_at))

    @commands.is_owner()
    @commands.command(name="gcban")
    async def gcban(self, ctx, user:int):
        await self.bot.gcserversdb.update_many({"_id": "servers"}, {"$push": {"blacklist": user}})

        try:
            user = await self.bot.fetch_user(user)
        except:
            return await ctx.send(embed=discord.Embed(title=f"{user} banned!"))

        globalchat_data = await self.bot.gcserversdb.find_one({"_id": "servers"})

        for channel in globalchat_data["channels"]:
            try:
                c = await self.bot.fetch_channel(channel)
                embed = discord.Embed(title=f"{user.name} banned!")
                embed.set_thumbnail(url=user.display_avatar.url)
                await c.send(embed=embed)
            except:
                continue

        return await ctx.author.send(embed=discord.Embed(title=f"{user.name} banned!"))

async def setup(bot):
    await bot.add_cog(Owner(bot))