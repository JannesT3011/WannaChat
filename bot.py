import discord
from discord.ext import commands
from discord import utils
from config import TOKEN, PREFIX, OWNERID, BLACKLIST_FILE_PATH, TOPGG_TOKEN, EMBED_COLOR
from database.database import DbClient, Database
import datetime
import requests
from checks import NotVoted, NotRegistered, NotGuild, NotPremium
from discord.ui import Button, View
import topgg
from cogs.profile import SelectView
from utils import get_logger

logger = get_logger("Bot")

COGS = [
    "cogs.help",
    "cogs.profile",
    "cogs.login",
    "cogs.swipe",
    #"cogs.globalchat",
    #"cogs.xp_coins",
    "cogs.convstarter",

    "cogs.test",

    "cogs.support.support",
    "cogs.owner.owner",
    "cogs.owner.sync",
    "cogs.owner.delete_user",

    "events.guild_join_login",

    "cogs.benefits.likedby",
    "cogs.benefits.reset",
    "cogs.benefits.profile_plus"
]

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super(Bot, self).__init__(
            command_prefix="wc.",
            description="Chat with someone random!",
            intents=intents,
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
        )
        self.launch = __import__("datetime").datetime.utcnow()
        self.version = "v1.5.11"
        self.creator = "Bambus#8446"
        self.ownerid = OWNERID
        self.test_guild = discord.Object(364335676549890048)

        self.db = DbClient().collection
        self.queuedb = DbClient().queuecollection
        self.gcserversdb = DbClient().gcserverscollection

        self.blacklist = self.load_blacklist()
        
        self.remove_command("bot")
        self.remove_command("help")

    def load_blacklist(self) -> list:
        my_file = open(BLACKLIST_FILE_PATH, "r")
        content = my_file.read()
        blacklist = content.split("\n")
        my_file.close()
        logger.info("Loaded blacklist!")

        return blacklist

    async def load_cogs(self):
        for ext in COGS:
            try:
                await self.load_extension(ext)
                logger.debug(f"Successfully loaded {ext}")
            except Exception as e:
                print(f"Cant load {ext}")
                raise e
    
    async def post_guild_count(self) -> None:
        """POST GUILD COUNT TO TOPGG"""
        topgg_client = topgg.DBLClient(self, TOPGG_TOKEN)
        await topgg_client.post_guild_count(len(self.guilds))
        await topgg_client.close()
        logger.info("Post Guild Count to Top.gg")

    async def on_ready(self):
        #await self.post_guild_count()

        # Add new field:
        #await self.db.update_many({}, {"$set": {"song": None}})
        logger.info("Bot started!")
        print(f"{self.user.id}\n"f"{utils.oauth_url(self.user.id)}\n"f"{self.user.name}\n""Ready!")

    async def on_message(self, message: discord.Message):
        """IGNORE BOT MESSAGES"""
        if message.author.bot:
            return

        await self.process_commands(message)

    async def on_guild_join(self, guild):
        await self.post_guild_count()

    async def on_guild_remove(self, guild):
        await self.post_guild_count()

    async def startup(self):
        await self.wait_until_ready()
        await self.tree.sync()

    async def setup_hook(self) -> None:
        self.tree.on_error = self.on_app_command_error
        await self.load_cogs()
        self.loop.create_task(self.startup())
        logger.info("Sync command and finisch setup hook")

    async def on_command_error(self, ctx, exception) -> None:
        if isinstance(exception, commands.CommandNotFound):
            return await ctx.send(embed=ErrorEmbed(f"This isn't a command! Please use the `{PREFIX}help` command"))

    async def on_app_command_error(self, interaction: discord.Interaction, error) -> None:
        if isinstance(error, commands.BotMissingAnyRole):
              return await interaction.response.send_message(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, discord.app_commands.MissingRole):
            return await interaction.response.send_message(embed=ErrorEmbed(str(error)))

        if isinstance(error, NotVoted):
            vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{self.user.id}/vote")
            view = View(timeout=None)
            view.add_item(vote_button)
            return await interaction.response.send_message(embed=discord.Embed(title="Please vote first to use this command!", url=f"https://top.gg/bot/{self.user.id}/vote", color=EMBED_COLOR), view=view)  
        
        elif isinstance(error, NotRegistered):
            embed = discord.Embed(title="You are not registered! 😔", description=f"Press the button to join the network and find new friends 🧑!\nTo see all commands use `{PREFIX}help`.", color=EMBED_COLOR)
            view = View(timeout=None)
            login_button = Button(label="Login", emoji="💬", style=discord.ButtonStyle.blurple) 

            async def login_button_interaction(interaction):
                try:
                    await Database().init_db(str(interaction.user.id))
                except:
                    return await interaction.user.send(embed=discord.Embed(title="Already login!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infors\nStart by selecting your gender:"), view=SelectView(author=interaction.user, bot=self)) # TODO buttons with profile options
                await self.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(interaction.user.id)}})
                await interaction.user.send(embed=discord.Embed(title="Login successful!", description=f"Type `{PREFIX}swipe` to start!\nStart by selecting your gender:", color=EMBED_COLOR).set_footer(text=f"Use `{PREFIX}help` to get more infos"), view=SelectView(author=interaction.user, bot=self))  
            
            login_button.callback = login_button_interaction
            view.add_item(login_button)

            return await interaction.response.send_message(embed=embed, view=view, ephemeral=True)   

        elif isinstance(error, NotGuild):
            return await interaction.response.send_message(embed=discord.Embed(title="You can only use this command on a server"), ephemeral=True)
        
        elif isinstance(error, NotPremium):
            premium_button = Button(label="Support me!", url="https://www.patreon.com/")
            view = View(timeout=None)
            view.add_item(premium_button)

            return await interaction.response.send_message(embed=discord.Embed(title="👑 Buy premium to use this command", color=EMBED_COLOR), view=view)

        elif isinstance(error, discord.app_commands.CheckFailure):
            return await interaction.response.send_message(embed=ErrorEmbed(str(error))) 

        elif isinstance(error, discord.app_commands.CommandNotFound):
            return await interaction.response.send_message(embed=ErrorEmbed(f"This isn't a command! Please use the `{PREFIX}help` command"))

        elif isinstance(error, discord.app_commands.CommandOnCooldown):
            return await interaction.response.send_message(embed=ErrorEmbed(f"Chill, you can use this command in {round(error.retry_after, 2)} seconds!"), delete_after=5)

        elif isinstance(error, discord.app_commands.CommandInvokeError):
            channel = self.get_channel(992779863855476826)
            return await channel.send(embed=ErrorEmbed(f"```{error}```"))

        else:
            channel = self.get_channel(992779863855476826)
            return await channel.send(embed=ErrorEmbed(f"```{error}```"))
    

bot = Bot()

class ErrorEmbed(discord.Embed):
    def __init__(self, description):
        super().__init__(
            title="Error",
            description=description,
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        self.set_footer(text=f"{bot.version} • made with ❤️ by {bot.creator}", icon_url=bot.user.display_avatar.url)

class OwnerErrorEmbed(discord.Embed):
    def __init__(self, description, server):
        super().__init__(
            title=f"Error on server {server}",
            description=f"```{description}```",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        self.set_footer(text=f"{bot.version} • made with ❤️ by {bot.creator}", icon_url=bot.user.display_avatar.url)

bot.run(TOKEN, reconnect=True)