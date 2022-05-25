import discord
from discord.ext import commands
from discord import utils
from config import TOKEN, PREFIX
import datetime

COGS = [
    "cogs.chat",
    "cogs.help"
]

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
            presences=True,
            invites=True
        )
        super(Bot, self).__init__(
            command_prefix=PREFIX,
            description="Chat with someone random!",
            intents=intents,
        )
        self.launch = __import__("datetime").datetime.utcnow()
        self.version = "0.0.1"
        self.creator = "Bambus#8446"

        self.remove_command("help")

        for ext in COGS:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f"Cant load {ext}")
                raise e
    
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f"{PREFIX}help"))
        print(f"{self.user.id}\n"f"{utils.oauth_url(self.user.id)}\n"f"{self.user.name}\n""Ready!")

    #async def on_message(self, message):
    #    """IGNORE PRIVATE MESSAGE"""
    #    if not message.guild:
    #        return
    #    await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=ErrorEmbed(str(error)))

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.BotMissingRole):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(embed=ErrorEmbed("This isn't a command! Please use the `help` command"))
        
        elif isinstance(error, commands.BadArgument):
            owner = self.get_user(self.owner_id)
            return await owner.send(embed=OwnerErrorEmbed(str(error), ctx.guild.name))

class ErrorEmbed(discord.Embed):
    def __init__(self, description):
        super().__init__(
            title="Error",
            description=description,
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        self.set_footer(text=f'{bot.user.name} made with <3 by Bambus#8446', icon_url=bot.user.avatar_url)

class OwnerErrorEmbed(discord.Embed):
    def __init__(self, description, server):
        super().__init__(
            title=f"Error on server {server}",
            description=f"```{description}```",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        self.set_footer(text=f'{bot.user.name} made with <3 by Bambus#8446', icon_url=bot.user.avatar_url)

bot = Bot()

bot.run(TOKEN)