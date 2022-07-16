import discord
from discord.ext import commands
from discord import utils
from config import TOKEN, PREFIX, OWNERID, BLACKLIST_FILE_PATH, TOPGG_TOKEN, EMBED_COLOR
from database.database import DbClient, Database
import datetime
import requests
from checks.voted import NotVoted
from checks.registered import NotRegistered
from discord.ui import Button, View

COGS = [
    "cogs.help",
    "cogs.profile",
    "cogs.login",
    "cogs.swipe",

    "cogs.support.support",
    "cogs.owner.owner",
    "cogs.owner.sync",

    "events.guild_join_login",
    "cogs.benefits.likedby",
    "cogs.benefits.reset"
]

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        super(Bot, self).__init__(
            command_prefix=PREFIX,
            description="Chat with someone random!",
            intents=intents,
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
        )
        self.launch = __import__("datetime").datetime.utcnow()
        self.version = "v1.4"
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

        data = {"server_count": len(self.guilds)}
        requests.post(f"https://top.gg/api/bots/{self.user.id}/stats", headers={"Authorization": TOPGG_TOKEN}, data=data)
        print(f"{self.user.id}\n"f"{utils.oauth_url(self.user.id)}\n"f"{self.user.name}\n""Ready!")

    async def on_message(self, message: discord.Message):
        """IGNORE BOT MESSAGES"""
        if message.author.bot:
            return
        if message.guild and message.content.startswith(PREFIX) and not message.content.startswith(f"{PREFIX}help"):
            try:
                return await message.author.send("Use me here, daddy!")
            except:
                return await message.send("Use me in my DMs, daddy!", delete_after=5)
        await self.process_commands(message)

    async def on_guild_join(self, guild):
        data = {"server_count": len(self.guilds)}
        requests.post(f"https://top.gg/api/bots/{self.user.id}/stats", headers={"Authorization": TOPGG_TOKEN}, data=data)

    async def on_guild_remove(self, guild):
        data = {"server_count": len(self.guilds)}
        requests.post("https://top.gg/api/bots/{self.user.id}/stats", headers={"Authorization": TOPGG_TOKEN}, data=data)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, commands.BotMissingRole):
            return await ctx.send(embed=ErrorEmbed(str(error)))
        
        elif isinstance(error, NotVoted):
            vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{self.user.id}/vote")
            view = View(timeout=None)
            view.add_item(vote_button)
            return await ctx.author.send(embed=discord.Embed(title="Please vote first to use this command!", url=f"https://top.gg/bot/{self.user.id}/vote", color=EMBED_COLOR), view=view)

        elif isinstance(error, NotRegistered):
            embed = discord.Embed(title="You are not registered! 😔", description=f"Press the button to join the network and find new friends 🧑!\nTo see all commands use `{PREFIX}help`.", color=EMBED_COLOR)
            view = View(timeout=None)
            login_button = Button(label="Login", emoji="💬", style=discord.ButtonStyle.blurple)

            async def login_button_interaction(interaction):
                try:
                    await Database().init_db(str(interaction.user.id))
                except:
                    return await interaction.user.send(embed=discord.Embed(title="Already login!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infors\nStart by selecting your gender:"), view=SelectView(author=interaction.user, bot=self.bot)) # TODO buttons with profile options
                await self.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(interaction.user.id)}})
                await interaction.user.send(embed=discord.Embed(title="Login successful!", description="Type `{PREFIX}swipe` to start!\nStart by selecting your gender:", color=EMBED_COLOR).set_footer(text=f"Use `{PREFIX}help` to get more infos"), view=SelectView(author=interaction.user, bot=self.bot))

            login_button.callback = login_button_interaction
            view.add_item(login_button)
            return await ctx.author.send(embed=embed, view=view)

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=ErrorEmbed(str(error)))

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(embed=ErrorEmbed(f"This isn't a command! Please use the `{PREFIX}help` command"))
        
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=ErrorEmbed(f"Chill, you can use this command in {round(error.retry_after, 2)} seconds!"), delete_after=5)
        
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

bot.run(TOKEN)