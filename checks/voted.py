from discord.ext import commands
import topgg
from config import TOPGG_TOKEN
import discord
from config import EMBED_COLOR, PREFIX
from discord.ui import Button, View

class NotVoted(discord.app_commands.CheckFailure):
    pass

def is_voter():
    async def predicate(interaction: discord.Interaction):
        topgg_client = topgg.DBLClient(interaction.client, TOPGG_TOKEN)
        check = await topgg_client.get_user_vote(interaction.user.id)
        await topgg_client.close()
        if check:
            return check
        raise NotVoted

    return discord.app_commands.check(predicate)

async def voted(bot, user) -> bool:
    topgg_client = topgg.DBLClient(bot, TOPGG_TOKEN)
    check = await topgg_client.get_user_vote(user.id)
    await topgg_client.close()
    if check:
        return check
    vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{bot.user.id}/vote")
    view = View(timeout=None)
    view.add_item(vote_button)
    await user.send(embed=discord.Embed(title="Please vote first to use this command!", url=f"https://top.gg/bot/{bot.user.id}/vote", color=EMBED_COLOR), view=view)
    return False