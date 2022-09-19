"""DELETE USER wc.userdel user"""
import discord
from discord import app_commands
from discord.ext import commands
from database.database import Database
from checks import is_owner

TEST_GUILD = discord.Object(364335676549890048)

class DelUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='deluser')
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def deluser(self, ctx, *, id:int):
        try:
            await Database().delete_db(str(id))
            await self.bot.queuedb.update_many({"_id": "queue"}, {"$pull": {"queue": str(id)}})
        except:
            return await ctx.send("Cant find this user")

        return await ctx.send(f"User {id} deleted!")

async def setup(bot):
    await bot.add_cog(DelUser(bot))