import discord
from discord.ext import commands
from config import PREFIX

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='profile', invoke_without_command=True)
    async def profile(self, ctx):
        try:
            data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        except:
            return await ctx.author.send("Please login first!", delete_after=4)
        embed = discord.Embed(title="Your profile")
        embed.add_field(name="Age", value=data["age"], inline=True)
        embed.add_field(name="Language", value=data["language"], inline=True)
        embed.add_field(name="Gender", value=data["gender"])
        if not len(data["interests"]) == 0:
            embed.add_field(name="Interests", value=", ".join(data['interests']), inline=False)
        if not data["aboutme"] == "":
            embed.add_field(name="About me", value=data["aboutme"], inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        #print(ctx.author.avatar_url)
        embed.set_footer(text=f"Set your age, language, gender, interests and about me with {PREFIX}profile <category>")
        return await ctx.author.send(embed=embed)
    
    @profile.command(name="age") # TODO check if user logins
    async def profile_age(self, ctx, age:str):
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"age": age}})
        except:
            return await ctx.author.send("Please login first!", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Age set to {age}"))
    
    @profile.command(name="language")
    async def profile_language(self, ctx, language):
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"language": language}})
        except:
            return await ctx.author.send("Please login first!", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Language set to {language}"))
    
    @profile.command(name="aboutme")
    async def profile_aboutme(self, ctx, *, aboutme:str):
        if len(aboutme) == 100:
            return await ctx.author.send("Aboutme can only be 100 characters long", delete_after=4)
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"aboutme": aboutme}})
        except:
            return await ctx.author.send("Please login first!", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Aboutme set to `{aboutme}`"))
    
    @profile.command(name="interests", aliases=["interest"]) # TODO remove interests
    async def profile_interest(self, ctx, *, interests):
        try:
            data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        except:
            return await ctx.author.send("Please login first!", delete_after=4)
        if len(data["interests"]) > 5:
            return await ctx.author.send("You can hav max. 5 interests!")

        await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$push": {"interests": interests}})
        return await ctx.author.send(embed=discord.Embed(title=f"Interest added: {interests}"))
    
    @profile.command(name="gender")
    async def profile_gender(self, ctx, gender):
        if not gender in ["male", "female", "divers"]:
            return await ctx.author.send("Invalid gender, please use: `male`, `female`, `divers`")
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"gender": gender}})
        except:
            return await ctx.author.send("Please login first!", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Gender set tot {gender}"))

async def setup(bot):
    await bot.add_cog(Profile(bot))