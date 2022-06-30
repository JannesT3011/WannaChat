import discord
from discord.ext import commands
from discord.ui import View, Button
from config import EMBED_COLOR, PREFIX
from database.database import Database

class GuildJoinLogin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = guild.system_channel
        embed = discord.Embed(title="Hey, I'm WannaChat! 👋🤖", description=f"Press the button to join the network and find new friends 🧑!\nTo see all commands use `{PREFIX}help`.", color=EMBED_COLOR)
        view = View(timeout=None)
        login_button = Button(label="Start", emoji="💬", style=discord.ButtonStyle.blurple)

        async def login_button_interaction(interaction):
            try:
                await Database().init_db(str(interaction.user.id))
            except:
                return await interaction.user.send(embed=discord.Embed(title="Already login!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infors"))
            await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(interaction.user.id)}})
            await interaction.user.send(embed=discord.Embed(title="Login successful!", description="Type `{PREFIX}swipe` to start!", color=EMBED_COLOR).set_footer(text=f"Use `{PREFIX}help` to get more infos"))

        login_button.callback = login_button_interaction
        view.add_item(login_button)

        try:
            await channel.send(embed=embed, view=view)
        except:
            pass

async def setup(bot):
    await bot.add_cog(GuildJoinLogin(bot))