import discord
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.command(name='bug')
    async def bug_report(self, ctx, *, bug):
        """REPORT A BUG"""
        if any(word in bug for word in self.bot.blacklist):
            return await ctx.send("Uh, dont use that word! 😞", delete_after=5)
        
        await self.bot.get_user(int(self.bot.ownerid)).send(embed=discord.Embed(title=f"Bug submitted by {ctx.author.name}#{ctx.author.discriminator}",description=f"```{bug}```"))
        
        return await ctx.author.send("Bug reported! Thank you!!")
    
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.command(name="suggestion")
    async def suggestion(self, ctx, *, idea):
        """SUBMIT A SUGGESTION"""
        if any(word in idea for word in self.bot.blacklist):
            return await ctx.send("Uh, dont use that word! 😞", delete_after=5)
        
        await self.bot.get_user(int(self.bot.ownerid)).send(embed=discord.Embed(title=f"Suggestion submitted by {ctx.author.name}#{ctx.author.discriminator}",description=f"```{idea}```"))
        
        return await ctx.author.send("Suggestion send! Thank you!!")


async def setup(bot):
    await bot.add_cog(Support(bot))