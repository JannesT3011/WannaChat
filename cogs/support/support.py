import discord
from discord import app_commands
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @app_commands.command(name="bug", description="Report a bug")
    async def bug_report(self, interaction: discord.Interaction, *, bug:str):
        """REPORT A BUG"""
        if any(word in bug for word in self.bot.blacklist):
            return await interaction.response.send_message("Uh, dont use that word! 😞", delete_after=5)
        
        owner = await self.bot.fetch_user(int(self.bot.ownerid))
        await owner.send(embed=discord.Embed(title=f"Bug submitted by {interaction.user.name}#{interaction.user.discriminator}",description=f"```{bug}```"))
        
        return await interaction.response.send_message("Bug reported! Thank you!!")
    
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @app_commands.command(name="suggestion", description="Suggest an idea")
    async def suggestion(self, interaction: discord.Interaction, *, idea:str):
        """SUBMIT A SUGGESTION"""
        if any(word in idea for word in self.bot.blacklist):
            return await interaction.response.send_message("Uh, dont use that word! 😞", delete_after=5)
        
        owner = await self.bot.fetch_user(int(self.bot.ownerid))
        await owner.send(embed=discord.Embed(title=f"Suggestion submitted by {interaction.user.name}#{interaction.user.discriminator}",description=f"```{idea}```"))
        
        return await interaction.response.send_message("Suggestion send! Thank you!!")


async def setup(bot):
    await bot.add_cog(Support(bot))