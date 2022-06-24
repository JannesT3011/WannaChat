import discord
from discord.ext import commands
from config import PREFIX, EMBED_COLOR


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='profile', invoke_without_command=True)
    async def profile(self, ctx):
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        if data is None:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        embed = discord.Embed(title="Your profile 🧑", color=EMBED_COLOR)
        embed.add_field(name="Age", value=data["age"], inline=True)
        embed.add_field(name="Language", value=", ".join(data["language"]), inline=True)
        embed.add_field(name="Gender", value=data["gender"])
        if not len(data["interests"]) == 0:
            embed.add_field(name="Interests", value=", ".join(data['interests']), inline=False)
        if not data["aboutme"] == "":
            embed.add_field(name="About me", value=data["aboutme"], inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"Set your age, language, gender, interests and about me with {PREFIX}profile <category>")
        return await ctx.author.send(embed=embed)
    
    @profile.command(name="age")
    async def profile_age(self, ctx, age:int):
        if age in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        if age > 119:
            return await ctx.author.send("I dont think the oldest person on this world is using this Bot 👵. But if you are, send me a message with: `wc.bug`")
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"age": age}})
        except:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Age set to {age}",color=EMBED_COLOR))
    
    @profile_age.error
    async def age_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.author.send("Urgg, Thats not a number...", delete_after=5)

    @profile.command(name="language")
    async def profile_language(self, ctx, subcommand, *,language):
        if language in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        try:
            data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        except:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)

        if subcommand == "add":
            language = language.split(" ")
            if len(language) > 1:
                return await ctx.author.send("Please use only one word, as language!", delete_after=5)
            
            language = language[0]
            if len(data["language"]) > 5:
                return await ctx.author.send("You can have max. 5 languages!")

            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$push": {"language": language.lower()}})
            return await ctx.author.send(embed=discord.Embed(title=f"Language added: {language}", color=EMBED_COLOR))

        if subcommand == "delete" or subcommand == "remove":
            if language not in data["language"]:
                return await ctx.author.send("Cant find that!", delete_after=5)
            
            if len(data["language"]) == 1:
                return await ctx.author.send("You need at least one language!")

            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$pull": {"language": language.lower()}})

            return await ctx.author.send(embed=f"{language} successfully removed!")
        
        else:
            return await ctx.author.send("Invalid argument, please use: `add`or `remove`")
    
    
    @profile.command(name="aboutme")
    async def profile_aboutme(self, ctx, *, aboutme:str):
        if len(aboutme) == 100:
            return await ctx.author.send("Aboutme can only be 100 characters long", delete_after=4)
        if any(word in aboutme for word in self.bot.blacklist):
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"aboutme": aboutme}})
        except:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Aboutme set to `{aboutme}`", color=EMBED_COLOR))
    
    @profile.command(name="interests", aliases=["interest"])
    async def profile_interest(self, ctx, subcommand, *, interests):
        if interests in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        try:
            data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        except:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)

        if subcommand == "add":
            interest = interests.split(" ")
            if len(interest) > 1:
                return await ctx.author.send("Please use only one word, as interest tag!", delete_after=5)
            
            interest = interest[0]
            if len(data["interests"]) > 5:
                return await ctx.author.send("You can have max. 5 interests!")

            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$push": {"interests": interest}})
            return await ctx.author.send(embed=discord.Embed(title=f"Interest added: {interest}", color=EMBED_COLOR))

        if subcommand == "delete" or subcommand == "remove":
            if interests not in data["interests"]:
                return await ctx.author.send("Cant find that!", delete_after=5)
            
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$pull": {"interests": interests}})

            return await ctx.author.send(f"{interests} successfully removed!")
        
        else:
            return await ctx.author.send("Invalid argument, please use: `add`or `remove`")
    
    @profile.command(name="gender")
    async def profile_gender(self, ctx, gender):
        if gender in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        if not gender in ["male", "female", "divers"]:
            return await ctx.author.send("Invalid gender, please use: `male`, `female`, `divers`")
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"gender": gender}})
        except:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)
        return await ctx.author.send(embed=discord.Embed(title=f"Gender set to {gender}", color=EMBED_COLOR))

async def setup(bot):
    await bot.add_cog(Profile(bot))