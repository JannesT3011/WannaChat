from discord.ext import commands
import topgg
from config import TOPGG_TOKEN

class NotVoted(commands.CheckFailure):
    pass

def is_voter():
    async def predicate(ctx):
        topgg_client = topgg.DBLClient(ctx.bot, TOPGG_TOKEN)
        check = await topgg_client.get_user_vote(ctx.author.id)
        await topgg_client.close()
        if check:
            return check
        raise NotVoted

    return commands.check(predicate)