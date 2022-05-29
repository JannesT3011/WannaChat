import discord
from discord.ext import commands
import random
from discord.ui import Button, View


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.group(name='chat', aliases=["wannachat"], invoke_without_command=True)
    async def chat(self, ctx):
        """SEARCH FOR CHATPARTNERS OR ADD YOU TO THE QUEUE"""
        if ctx.author.bot:
            return
        if len(self.queue) == 0:
            self.queue.append(ctx.author.id)
            return await ctx.reply("There is no other user searching, I put you in the waiting queue! I'll send you a message when someone wanna chat", delete_after=5)
        
        if ctx.author.id in self.queue:
            return await ctx.reply("You are in the waiting queue!", delete_after=4)
        
        user = random.choice(self.queue)
        while user == ctx.author.id:
            user = random.choice(self.queue)
        
        user = self.bot.get_user(user)

        # REMOVE AUTHOR AND CHAT PARTNER FROM QUEUE
        self.queue.remove(user.id)
        self.queue.remove(ctx.author.id)

        return await ctx.author.send(embed=discord.Embed(title="Wanna chat with:", description=f"Add: `{user.name}#{user.discriminator}`").set_thumbnail(url=user.avatar_url))

    @chat.command(name="remove")
    async def chat_remove(self, ctx):
        """REMOVES USER FROM QUEUE"""
        self.queue.remove(ctx.author.id)

        async def button_interaction(interaction):
            await interaction.response.edit_message(embed=discord.Embed(title=random.randint(1,10)))

        like_button = Button(label="Like!", style=discord.ButtonStyle.green, emoji="❤️") # TODO das für tinder bloß mit profile embed ersetzen!
        dislike_button = Button(label="Nah", style=discord.ButtonStyle.red, emoji="💤") # TODO error handler -> on_timeout -> delete message
        like_button.callback = button_interaction
        dislike_button.callback = button_interaction
        view = View()
        view.add_item(like_button)
        view.add_item(dislike_button)
        return await ctx.reply(embed=discord.Embed(title="Successfully removed you from the waiting queue!"), view=view)

async def setup(bot):
    await bot.add_cog(Chat(bot))