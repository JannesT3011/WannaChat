import discord
from discord import app_commands
from discord.ext import commands
from config import PREFIX, EMBED_COLOR, SUPPORT_SERVER_LINK
from discord.ui import Button, View

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="See all commands")
    async def help(self, interaction: discord.Interaction):
        """HELP COMMAND"""
        embed = discord.Embed(title="WannaChat - Help", description="Swipe to find random chat partners!\nSlide in my DMs to use me 🏄\n<> are required arguments, you DONT need to type `<>`!", color=EMBED_COLOR)
        embed.add_field(name="How to start:", value=f"1. Login with `{PREFIX}login`\n"
        f"2. Update your profile (see command list)\n"
        f"3. Start swiping and find your chatpartner with `{PREFIX}swipe`!\n"
        f"4. Have fun and start chatting! 🔥\n",
        inline=False)
        embed.add_field(name="Commands", value=f"`{PREFIX}login`: Create an account\n"
        f"`{PREFIX}logout`: Delete your account\n"
        f"`{PREFIX}profile`: View your profile\n"
        f"`{PREFIX}age <age>`: Set your age\n"
        f"`{PREFIX}language view`: View your current languages\n"
        f"`{PREFIX}language add <language>`: Set your language\n"
        f"`{PREFIX}language remove`: Remove a language\n"
        f"`{PREFIX}gender <gender>`: Set your gender\n"
        f"`{PREFIX}interests view`: View your current interests\n"
        f"`{PREFIX}interests add <interest>`: Set your interest\n"
        f"`{PREFIX}interests remove`: Remove interest\n"
        f"`{PREFIX}aboutme <aboutme_text>`: Set your AboutMe text\n",
        inline=False)
        embed.add_field(name="Voting benefit commands", value=f"`{PREFIX}likedby`: See the users who liked you\n"
        f"`{PREFIX}reset`: Reset your likes and dislikes\n"
        f"`{PREFIX}reset likes`: Reset your likes\n"
        f"`{PREFIX}reset dislikes`: Reset your dislikes\n", 
        inline=False)
        embed.add_field(name="Support", value=f"`{PREFIX}bug <bug>`: Report a bug\n" 
        f"`{PREFIX}suggestions <suggestion>`: Submit new feature suggestionn\nOr join the [support server]( {SUPPORT_SERVER_LINK} )\n"
        "To support and grow the Bot you can vote. This helps me to grow and brings new users, so you can make new friends.😊")
        embed.set_footer(text=f"{self.bot.version} • made with ❤️ by {self.bot.creator}", icon_url=self.bot.user.display_avatar.url)

        invite_button = Button(label="Add me to your server", url="https://discord.com/oauth2/authorize?client_id=979065679376437308&scope=bot+applications.commands&permissions=414464724032")
        vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{self.bot.user.id}/vote")
        view = View()
        view.add_item(invite_button)
        view.add_item(vote_button)
        
        return await interaction.response.send_message(embed=embed, view=view)
    
    #@help.command(name="profile")
    #async def profile_command(self, interaction: discord.Interaction):
    #    """PROFILE HELP COMMAND"""
    #    embed = discord.Embed(title="WannaChat - Profile help", description="Swipe to find random chat partners!\nUse me in my DMs\n<> are required arguments, you DONT need to type `<>`!", color=EMBED_COLOR, timestamp=ctx.message.created_at)
    #    embed.add_field(name="Profile commands", value=f"`{PREFIX}profile`: View your profile\n"
    #    f"`{PREFIX}profile`: View your profile\n"
    #    f"`{PREFIX}age <age>`: Set your age\n"
    #    f"`{PREFIX}language`: View your current languages\n"
    #    f"`{PREFIX}language add <language>`: Set your language\n"
    #    f"`{PREFIX}language remove <language>`: Remove a language\n"
    #    f"`{PREFIX}gender <gender>`: Set your gender\n"
    #    f"`{PREFIX}interests`: View your current interests\n"
    #    f"`{PREFIX}interests add <interest>`: Set your interest\n"
    #    f"`{PREFIX}interests remove <interest>`: Remove interest\n"
    #    f"`{PREFIX}aboutme <aboutme_text>`: Set your AboutMe text\n",
    #    inline=False)
    #    embed.set_footer(text=f"{self.bot.version} • made with ❤️ by {self.bot.creator}", icon_url=self.bot.user.display_avatar.url)
    #    
    #    invite_button = Button(label="Add me to your server", url="https://discord.com/oauth2/authorize?client_id=979065679376437308&scope=bot+applications.commands&permissions=414464724032")
    #    vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{self.bot.user.id}/vote")
    #    view = View()
    #    view.add_item(invite_button)
    #    view.add_item(vote_button)
#
    #    return await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))