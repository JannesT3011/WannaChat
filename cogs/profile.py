import discord
from discord.ext import commands
from config import PREFIX, EMBED_COLOR
from checks.registered import is_registered

class GenderSelect(discord.ui.Select):
    def __init__(self, author: discord.User, bot):
        self.author = author
        self.bot = bot
        options = [            
            discord.SelectOption(label="Male",emoji="♂️",),
            discord.SelectOption(label="Female",emoji="♀️"),
            discord.SelectOption(label="Divers",emoji="🧑")
        ]
        super().__init__(placeholder="Select your gender", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            await self.bot.db.update_many({"_id": str(self.author.id)}, {"$set": {"gender": self.values[0]}})
        except:
            return await interaction.response.send_message(f"Please use `{PREFIX}login` first")
            
        return await interaction.response.send_message(embed=discord.Embed(title=f"Gender set to {self.values[0]}", color=EMBED_COLOR))


class SelectView(discord.ui.View):
    def __init__(self, *, author:discord.User, bot, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(GenderSelect(author=author, bot=bot))

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @is_registered()
    @commands.command(name="profile", aliases=["p"])
    async def profile(self, ctx):
        """VIEW PROFILE"""
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})

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

        return await ctx.author.send(embed=embed, view=SelectView(author=ctx.author, bot=self.bot))
    
    @is_registered()
    @commands.command(name="age", aliases=["a"])
    async def profile_age(self, ctx, age:int):
        """SET YOUR PROFILE AGE"""
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
        """AGE ERROR HANDLER"""
        if isinstance(error, commands.BadArgument):
            return await ctx.author.send("Urgg, Thats not a number...", delete_after=5)

    @is_registered()
    @commands.group(name="language", aliases=["languages", "l"], invoke_without_command=True) 
    async def language(self, ctx):
        """SET YOUR PROFILE LANGUAGE"""
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
            
        return await ctx.author.send(embed=discord.Embed(title="Your current languages:", description=", ".join(data["language"])).set_footer(text=f"Use: {PREFIX}language <add/delete> to add/delete a language"))
    
    @is_registered()
    @language.command(name="add", aliases=["a"])
    async def language_add(self, ctx, language:str):
        if language in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)

        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        
        if len(data["language"]) > 5:
            return await ctx.author.send("You can have max. 5 languages!")
        
        if language in data["language"]:
            return await ctx.author.send("Language already added!")
        await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$push": {"language": language.lower()}})

        return await ctx.author.send(embed=discord.Embed(title=f"Language added: {language}", color=EMBED_COLOR))
    
    @is_registered()
    @language.command(name="delete", aliases=["remove", "del", "r"])
    async def language_delete(self, ctx, language:str):
        if language in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
            
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})
        
        if language not in data["language"]:
            return await ctx.author.send(embed=discord.Embed(title=f"Language removed: {language}", color=EMBED_COLOR))
        
        if len(data["language"]) == 1:
            return await ctx.author.send("You need at least one language!")
        await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$pull": {"language": language.lower()}})

        return await ctx.author.send(f"{language} successfully removed!")
    
    @is_registered()
    @commands.command(name="aboutme", aliases=["am"])
    async def profile_aboutme(self, ctx, *, aboutme:str):
        """SET YOUR PROFILE ABOUTME"""
        if len(aboutme) == 100:
            return await ctx.author.send("Aboutme can only be 100 characters long", delete_after=4)
        if any(word in aboutme for word in self.bot.blacklist):
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        try:
            await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$set": {"aboutme": aboutme}})
        except:
            return await ctx.author.send(f"Please use `{PREFIX}login` first", delete_after=4)

        return await ctx.author.send(embed=discord.Embed(title=f"Aboutme set to `{aboutme}`", color=EMBED_COLOR))
    
    @is_registered()
    @commands.group(name="interests", aliases=["interest"], invoke_without_command=True)
    async def interests(self, ctx):
        """SET YOUR PROFILE INTERESTS"""
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})

        return await ctx.author.send(embed=discord.Embed(title="Your current interests:", description=", ".join(data["interests"])).set_footer(text=f"Use: {PREFIX}interests <add/delete> to add/delete a interests"))
    
    @is_registered()
    @interests.command(name="add", aliases=["a"])
    async def interest_add(self, ctx, *, interests:str):
        """ADD INTEREST"""
        if interests in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)

        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})

        interest = interests.split(" ")

        if len(interest) > 1:
            return await ctx.author.send("Please use only one word, as interest tag!", delete_after=5)
        
        interest = interest[0]
        if len(data["interests"]) > 5:
            return await ctx.author.send("You can have max. 5 interests!")
        await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$push": {"interests": interest}})

        return await ctx.author.send(embed=discord.Embed(title=f"Interest added: {interest}", color=EMBED_COLOR))
    
    @is_registered()
    @interests.command(name="delete", aliases=["remove", "r"])
    async def interest_delete(self, ctx, *, interests:str):
        """DELETE A INTEREST"""
        if interests in self.bot.blacklist:
            return await ctx.author.send("Uh, dont use that word! 😞", delete_after=5)
        
        data = await self.bot.db.find_one({"_id": str(ctx.author.id)})

        if interests not in data["interests"]:
            return await ctx.author.send("Cant find that!", delete_after=5)
        
        await self.bot.db.update_many({"_id": str(ctx.author.id)}, {"$pull": {"interests": interests}})
        return await ctx.author.send(embed=discord.Embed(title=f"Interest removed: {interests}", color=EMBED_COLOR))
    
    @is_registered()
    @commands.command(name="gender", aliases=["g"])
    async def profile_gender(self, ctx):
        """SET YOUR PROFILE GENDER"""

        return await ctx.author.send(view=SelectView(author=ctx.author, bot=self.bot))

async def setup(bot):
    await bot.add_cog(Profile(bot))