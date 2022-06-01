import discord
from discord.ext import commands
from discord import utils
from config import TOKEN, PREFIX, OWNERID, BLACKLIST_FILE_PATH
from database.database import DbClient, Database
import datetime


COGS = [
    "cogs.help",
    "cogs.profile",
    "cogs.login",
    "cogs.tinder",

    "cogs.support.support"
]

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents.all()
        super(Bot, self).__init__(
            command_prefix=PREFIX,
            description="Chat with someone random!",
            intents=intents,
        )
        self.launch = __import__("datetime").datetime.utcnow()
        self.version = "v0.1.1"
        self.creator = "Bambus#8446"
        self.ownerid = OWNERID
        self.db = DbClient().collection
        self.queuedb = DbClient().queuecollection
        self.blacklist = self.load_blacklist()
        
        self.remove_command("bot")
        self.remove_command("help")

    def load_blacklist(self) -> list:
        my_file = open(BLACKLIST_FILE_PATH, "r")
        content = my_file.read()
        blacklist = content.split("\n")
        my_file.close()

        return blacklist

    async def load_cogs(self):
        for ext in COGS:
            try:
                await self.load_extension(ext)
            except Exception as e:
                print(f"Cant load {ext}")
                raise e
    
    async def on_ready(self):
        await self.load_cogs()
        await self.change_presence(activity=discord.Game(name=f"{PREFIX}help"))
        print(f"{self.user.id}\n"f"{utils.oauth_url(self.user.id)}\n"f"{self.user.name}\n""Ready!")

    async def on_message(self, message: discord.Message):
        """IGNORE BOT MESSAGES"""
        if message.author.bot:
            return
        if message.guild and message.content.startswith(PREFIX) and not message.content.startswith(f"{PREFIX}help"):
            return await message.author.send("Use me here, daddy!")
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.BotMissingRole):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(embed=ErrorEmbed("This isn't a command! Please use the `help` command"))
        
        elif isinstance(error, commands.BadArgument):
            owner = self.get_user(self.ownerid)
            return await owner.send(embed=OwnerErrorEmbed(str(error), ctx.guild.name))

class ErrorEmbed(discord.Embed):
    def __init__(self, description):
        super().__init__(
            title="Error",
            description=description,
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        #self.set_footer(text=f'{bot.user.name} made with <3 by Bambus#8446', icon_url=bot.user.avatar_url)

class OwnerErrorEmbed(discord.Embed):
    def __init__(self, description, server):
        super().__init__(
            title=f"Error on server {server}",
            description=f"```{description}```",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        #self.set_footer(text=f'{bot.user.name} made with <3 by Bambus#8446', icon_url=bot.user.avatar_url)

bot = Bot()

bot.run(TOKEN)