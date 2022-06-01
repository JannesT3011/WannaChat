import discord
from discord.ext import commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def name_command(self, ctx):
        embed = discord.Embed(title="WannaChat - Help", description="Swipe to find random chat partners!\nUse me in my DMs\n<> are required arguments", color=EMBED_COLOR)
        embed.add_field(name="How to start:", value=f"1. Login with `{PREFIX}login`\n"
        f"2. Update your profile with `{PREFIX}profile <category>`\n"
        f"3. Start swiping and find your chatpartner with `{PREFIX}swipe`!\n"
        f"4. Have fun and start chatting! 🔥\n",
        inline=False)
        embed.add_field(name="Commands", value=f"`{PREFIX}login`: Create an account\n"
        f"`{PREFIX}logout`: Delete your account\n"
        f"`{PREFIX}profile`: View your profile\n"
        f"`{PREFIX}profile age <age>`: Set your age\n"
        f"`{PREFIX}profile language add <language>`: Set your language\n"
        f"`{PREFIX}profile language remove <language>`: Remove a language\n"
        f"`{PREFIX}profile gender <gender>`: Set your gender\n"
        f"`{PREFIX}profile interests add <interest>`: Set your interest\n"
        f"`{PREFIX}profile interests remove <interest>`: Remove interest\n"
        f"`{PREFIX}profile aboutme <aboutme_text>`: Set your AboutMe text\n",
        inline=False)
        embed.add_field(name="Support", value=f"`{PREFIX}bug <bug>`: Report a bug\n" 
        f"`{PREFIX}suggestions <suggestion>`: Submit new feature suggestion")
        embed.set_footer(text=f"{self.bot.version} • made with ❤️ by {self.bot.creator}")

        invite_button = Button(label="Add me to your server", url="https://discord.com/oauth2/authorize?client_id=979065679376437308&scope=bot+applications.commands")
        view = View()
        view.add_item(invite_button)
        
        return await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))