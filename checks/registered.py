from discord.ext import commands
import topgg
from config import TOPGG_TOKEN
import discord
from database.database import Database
from discord.ui import Button, View
from config import PREFIX, EMBED_COLOR
from utils import get_logger

logger = get_logger("Registered")

class NotRegistered(discord.app_commands.CheckFailure):
    pass

def is_registered():
    async def predicate(interaction: discord.Interaction):
        data = await interaction.client.db.find_one({"_id": str(interaction.user.id)})
        if data is None:
            raise NotRegistered
        return True

    return discord.app_commands.check(predicate)

async def registered(bot, user) -> bool:
    data = await bot.db.find_one({"_id": str(user.id)})
    if data is None:
        embed = discord.Embed(title="You are not registered! 😔", description=f"Press the button to join the network and find new friends 🧑!\nTo see all commands use `{PREFIX}help`.", color=EMBED_COLOR)
        view = View(timeout=None)
        login_button = Button(label="Login", emoji="💬", style=discord.ButtonStyle.blurple)
        async def login_button_interaction(interaction):
            try:
                await Database().init_db(str(interaction.user.id))
            except:
                return await interaction.user.send(embed=discord.Embed(title="Already login!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infors\nStart by selecting your gender:"), view=SelectView(author=interaction.user, bot=bot)) # TODO buttons with profile options
            await bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(interaction.user.id)}})
            await interaction.user.send(embed=discord.Embed(title="Login successful!", description=f"Type `{PREFIX}swipe` to start!\nStart by selecting your gender:", color=EMBED_COLOR).set_footer(text=f"Use `{PREFIX}help` to get more infos"), view=SelectView(author=interaction.user, bot=bot))
        login_button.callback = login_button_interaction
        view.add_item(login_button)
        try:
            await user.send(embed=embed, view=view)
        except discord.errors.Forbidden:
            logger.debug("Cannot send message to this user.")

        return False
    return True