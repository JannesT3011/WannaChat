import discord
from discord.ext import commands
from config import PREFIX

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def name_command(self, ctx):
        embed = discord.Embed(title="WannaChat - Help")
        embed.add_field(name="Chat commands", value="`{PREFIX}.chat`: Send you a random user from the queue, you can chat with!")
        return await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))