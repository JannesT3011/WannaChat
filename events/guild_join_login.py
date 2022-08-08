import discord
from discord.ext import commands
from discord.ui import View, Button
from config import EMBED_COLOR, PREFIX
from database.database import Database

from cogs.profile import SelectView

class GuildJoinLogin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild): 
        channel = guild.system_channel
        embed = discord.Embed(title="Hey, I'm WannaChat! 👋🤖", description=f"Press the button to join the network and find new friends 🧑!\nTo see all commands use `{PREFIX}help`.", color=EMBED_COLOR)
        embed.add_field(name="🌐GlobalChat", value="You can also use the GlobalChat, select one channel and type `/globalchat activate`")
        view = View(timeout=None)
        login_button = Button(label="Start", emoji="💬", style=discord.ButtonStyle.blurple)

        async def login_button_interaction(interaction):
            try:
                await Database().init_db(str(interaction.user.id))
            except:
                return await interaction.user.send(embed=discord.Embed(title="Already login!", description=f"Use `{PREFIX}swipe` to find a chatpartner or `{PREFIX}help` to get more infors\nStart by selecting your gender:"), view=SelectView(author=interaction.user, bot=self.bot)) # TODO buttons with profile options
            await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(interaction.user.id)}})
            await interaction.user.send(embed=discord.Embed(title="Login successful!", description="Type `{PREFIX}swipe` to start!\nStart by selecting your gender:", color=EMBED_COLOR)
            .add_field(name="Your next steps:", value=f"➡️ Set your age with `{PREFIX}age`\n➡️ Add languages with `{PREFIX}language add`\n➡️ Add your interests with `{PREFIX}interest add`\n➡️ Set your AboutMe text with `{PREFIX}aboutme`")
            .set_footer(text=f"Use `{PREFIX}help` to get more infos"), 
            view=SelectView(author=interaction.user, bot=self.bot))

        login_button.callback = login_button_interaction
        view.add_item(login_button)

        try:
            await channel.send(embed=embed, view=view)
        except:
            pass

async def setup(bot):
    await bot.add_cog(GuildJoinLogin(bot))