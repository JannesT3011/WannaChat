import discord
from utils import get_logger

logger = get_logger("Premium")

class NotPremium(discord.app_commands.CheckFailure):
    pass

def is_premium():
    async def predicate(interaction: discord.Interaction):
        data = await interaction.client.db.find_one({"_id": str(interaction.user.id)})
        if data["premium"] == 0:
            raise NotPremium
        return True

    return discord.app_commands.check(predicate)