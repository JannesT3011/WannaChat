"""RESET DISLIKED USERS

ALSO RESET LIKED USERS
"""

import discord
from discord.ext import commands
from config import PREFIX, EMBED_COLOR
from discord.ui import Button, View
from checks.voted import is_voter

class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @commands.group(name='reset', aliases=["r"], invoke_without_command=True)
    async def reset(self, ctx):
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        if data is None:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        
        async def confirm_button_interaction(interaction):
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"disliked_users": []}})
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"liked_users": []}})

            await msg.delete()
            return await ctx.author.send(embed=discord.Embed(title="Successfully reseted your liked and disliked users!", color=EMBED_COLOR))

        async def cancel_button_interaction(interaction):
            return await msg.delete()

        confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
        confirm_button.callback = confirm_button_interaction
        cancel_button.callback = cancel_button_interaction
        view = View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)

        msg = await ctx.author.send(embed=discord.Embed(title="Are you sure you want to reset your liked and disliked users?", color=EMBED_COLOR), view=view)

    @is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @reset.command(name="likes", aliases=["l"])
    async def reset_likes(self, ctx):
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        if data is None:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        
        async def confirm_button_interaction(interaction):
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"liked_users": []}})
            await msg.delete()
            return await ctx.author.send(embed=discord.Embed(title="Successfully reseted your liked users!", color=EMBED_COLOR))
        
        async def cancel_button_interaction(interaction):
            return await msg.delete()

        confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
        confirm_button.callback = confirm_button_interaction
        cancel_button.callback = cancel_button_interaction
        view = View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)

        msg = await ctx.author.send(embed=discord.Embed(title="Are you sure you want to reset your liked users?", color=EMBED_COLOR), view=view)

    @is_voter()
    @commands.cooldown(1, 180.0, commands.BucketType.user)
    @reset.command(name="dislikes", aliases=["dl"])
    async def reset_dislikes(self, ctx):
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        if data is None:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        
        async def confirm_button_interaction(interaction):
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"disliked_users": []}})
            await msg.delete()
            return await ctx.author.send(embed=discord.Embed(title="Successfully reseted your disliked users!", color=EMBED_COLOR))
        
        async def cancel_button_interaction(interaction):
            return await msg.delete()

        confirm_button = Button(label="Yes", style=discord.ButtonStyle.red, emoji="✅")
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.green, emoji="❌")
        confirm_button.callback = confirm_button_interaction
        cancel_button.callback = cancel_button_interaction
        view = View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)

        msg = await ctx.author.send(embed=discord.Embed(title="Are you sure you want to reset your disliked users?", color=EMBED_COLOR), view=view)


async def setup(bot):
    await bot.add_cog(Reset(bot))