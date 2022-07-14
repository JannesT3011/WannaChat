from discord.ext import commands
import topgg
from config import TOPGG_TOKEN

class NotRegistered(commands.CheckFailure):
    pass

def is_registered():
    async def predicate(ctx):
        data = await ctx.bot.db.find_one({"_id": str(ctx.author.id)})
        if data is None:
            raise NotRegistered
        return True

    return commands.check(predicate)