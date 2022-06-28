import discord
from discord.ext import commands
from database.database import Database
from config import EMBED_COLOR
from discord.ui import Button, View

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='login', aliases=["create"])
    async def login(self, ctx):
        """LOGIN/CREATE YOUR ACCOUNT"""
        try:
            await Database().init_db(str(ctx.author.id))
        except:
            return await ctx.author.send("Already login!", delete_after=4)
        await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(ctx.author.id)}})
        return await ctx.author.send(embed=discord.Embed(title="Login successful!", color=EMBED_COLOR))
    
    @commands.command(name="logoff", aliases=["delete"])
    async def logoff(self, ctx):
        """LOGOFF/DELETE YOUR ACCOUNT"""
        async def logoff_confirm_button(interaction):
            try:
                await Database().delete_db(str(ctx.author.id))
            except:
                await msg.delete()
                return await ctx.author.send("Already logoff!")
            await self.bot.queuedb.update_many({"_id": "queue"}, {"$pull": {"queue": str(ctx.author.id)}})

            await msg.delete()
            return await ctx.author.send(embed=discord.Embed(title="Logoff successful!", description="Type `{PREFIX}swipe` to start!", color=EMBED_COLOR))

        async def logoff_cancel_button(interaction):
            return await msg.delete()

        confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
        confirm_button.callback = logoff_confirm_button
        cancel_button.callback = logoff_cancel_button
        view = View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)
        msg = await ctx.author.send(embed=discord.Embed(title="Are you sure you want to delete your account?", color=EMBED_COLOR), view=view)

async def setup(bot):
    await bot.add_cog(Login(bot))