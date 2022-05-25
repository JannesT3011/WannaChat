import discord
from discord.ext import commands
import random

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.group(name='chat', aliases=["wannachat"], invoke_without_command=True)
    async def chat(self, ctx):
        """SEARCH FOR CHATPARTNERS OR ADD YOU TO THE QUEUE"""
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

        return await ctx.author.send(embed=discord.Embed(title="I find someone to chat with:", description=f"Add: `{user.name}#{user.discriminator}`").set_thumbnail(url=user.avatar_url))

    @chat.command(name="remove")
    async def chat_remove(self, ctx):
        """REMOVES USER FROM QUEUE"""
        self.queue.remove(ctx.author.id)

        return await ctx.reply("Successfully removed you from the waiting queue!", delete_after=4)

def setup(bot):
    bot.add_cog(Chat(bot))