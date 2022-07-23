import discord
from discord.ext import commands
from discord import app_commands
from config import PREFIX, EMBED_COLOR
from checks.registered import is_registered, registered

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
        await self.bot.db.update_many({"_id": str(self.author.id)}, {"$set": {"gender": self.values[0]}})
            
        return await interaction.response.send_message(embed=discord.Embed(title=f"Gender set to {self.values[0]}", color=EMBED_COLOR), ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, author:discord.User, bot, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(GenderSelect(author=author, bot=bot))


class InterestSelect(discord.ui.Select):
    def __init__(self, author: discord.User, bot, interests:list):
        self.author = author
        self.bot = bot
        options = [discord.SelectOption(label=interest) for interest in interests]
        super().__init__(placeholder="Select the interest you like to remove", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
       await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$pull": {"interests": self.values[0]}})
           
       return await interaction.response.send_message(embed=discord.Embed(title=f"Interest removed: {self.values[0]}", color=EMBED_COLOR), ephemeral=True)

class InterestSelectView(discord.ui.View):
    def __init__(self, *, author:discord.User, bot, interests:list, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(InterestSelect(author=author, bot=bot, interests=interests))


class LanguageSelect(discord.ui.Select):
    def __init__(self, author: discord.User, bot, language:list):
        self.author = author
        self.bot = bot
        options = [discord.SelectOption(label=language) for language in language]
        super().__init__(placeholder="Select the language you like to remove", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
       await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$pull": {"language": self.values[0]}})
           
       return await interaction.response.send_message(embed=discord.Embed(title=f"Language removed: {self.values[0]}", color=EMBED_COLOR), ephemeral=True)

class LanguageSelectView(discord.ui.View):
    def __init__(self, *, author:discord.User, bot, language:list, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(LanguageSelect(author=author, bot=bot, language=language))


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@is_registered()
    @app_commands.command(name="profile", description="View your profile")
    async def profile(self, interaction: discord.Interaction):
        """VIEW PROFILE"""
        if await registered(self.bot, interaction.user):
            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})

            embed = discord.Embed(title="Your profile 🧑", color=EMBED_COLOR)
            embed.add_field(name="Age", value=data["age"], inline=True)
            embed.add_field(name="Language", value=", ".join(data["language"]), inline=True)
            embed.add_field(name="Gender", value=data["gender"])
            if not len(data["interests"]) == 0:
                embed.add_field(name="Interests", value=", ".join(data['interests']), inline=False)
            if not data["aboutme"] == "":
                embed.add_field(name="About me", value=data["aboutme"], inline=False)
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.set_footer(text=f"See how you modify your profile with {PREFIX}help")

            return await interaction.response.send_message(embed=embed, view=SelectView(author=interaction.user, bot=self.bot), ephemeral=True)
        
    #@is_registered()
    @app_commands.command(name="age", description="Set your age")
    async def profile_age(self, interaction: discord.Interaction, age:int):
        """SET YOUR PROFILE AGE"""
        if await registered(self.bot, interaction.user):
            if age in self.bot.blacklist:
                return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)
            if age > 119:
                return await interaction.response.send_message("I dont think the oldest person on this world is using this Bot 👵. But if you are, send me a message with: `wc.bug`")
            try:
                await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"age": age}})
            except:
                return await interaction.response.send_message(f"Please use `{PREFIX}login` first", ephemeral=True)

            return await interaction.response.send_message(embed=discord.Embed(title=f"Age set to {age}",color=EMBED_COLOR), ephemeral=True)
        
    @profile_age.error
    async def age_error(self, interaction: discord.Interaction, error):
        """AGE ERROR HANDLER"""
        if isinstance(error, commands.BadArgument):
            return await interaction.response.send_message("Urgg, Thats not a number...", ephemeral=True)

    language_group = app_commands.Group(name="language", description="See, add or remove your languages")

    #@is_registered()
    @language_group.command(name="view", description="See your current languages") 
    async def language(self, interaction: discord.Interaction):
        """SET YOUR PROFILE LANGUAGE"""
        if await registered(self.bot, interaction.user):
            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
                
            return await interaction.response.send_message(embed=discord.Embed(title="Your current languages:", description=", ".join(data["language"])).set_footer(text=f"Use: {PREFIX}language <add/delete> to add/delete a language"), ephemeral=True)
        
    #@is_registered()
    @language_group.command(name="add", description="Add one language")
    async def language_add(self, interaction: discord.Interaction, language:str):
        if await registered(self.bot, interaction.user):
            if language in self.bot.blacklist:
                return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)

            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
            
            if len(data["language"]) > 5:
                return await interaction.response.send_message("You can have max. 5 languages!")
            
            if language in data["language"]:
                return await interaction.response.send_message("Language already added!")
            await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$push": {"language": language.lower()}})

            return await interaction.response.send_message(embed=discord.Embed(title=f"Language added: {language}", color=EMBED_COLOR), ephemeral=True)
        
    #@is_registered()
    @language_group.command(name="remove", description="Remove a language")
    async def language_delete(self, interaction: discord.Interaction):
        if await registered(self.bot, interaction.user):
            languages = await self.bot.db.find_one({"_id": str(interaction.user.id)})
            return await interaction.response.send_message(view=LanguageSelectView(author=interaction.user, bot=self.bot, language=languages["language"]), ephemeral=True)

    #@is_registered()
    @app_commands.command(name="aboutme", description="Set your AboutMe description")
    async def profile_aboutme(self, interaction: discord.Interaction, *, aboutme:str):
        """SET YOUR PROFILE ABOUTME"""
        if await registered(self.bot, interaction.user):
            if len(aboutme) == 100:
                return await interaction.response.send_message("Aboutme can only be 100 characters long", ephemeral=True)
            if any(word in aboutme for word in self.bot.blacklist):
                return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)
            try:
                await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"aboutme": aboutme}})
            except:
                return await interaction.response.send_message(f"Please use `{PREFIX}login` first", ephemeral=True)

            return await interaction.response.send_message(embed=discord.Embed(title=f"Aboutme set to `{aboutme}`", color=EMBED_COLOR), ephemeral=True)
        
    interest_group = app_commands.Group(name="interests", description="View, add and remove your interests")

    #@is_registered()
    @interest_group.command(name="view", description="See your interests")
    async def interests(self, interaction: discord.Interaction):
        """SET YOUR PROFILE INTERESTS"""
        if await registered(self.bot, interaction.user):
            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})

            return await interaction.response.send_message(embed=discord.Embed(title="Your current interests:", description=", ".join(data["interests"])).set_footer(text=f"Use: {PREFIX}interests <add/delete> to add/delete a interests"), ephemeral=True)
        
    #@is_registered()
    @interest_group.command(name="add", description="Add a interest")
    async def interest_add(self, interaction: discord.Interaction, *, interests:str):
        """ADD INTEREST"""
        if await registered(self.bot, interaction.user):
            if interests in self.bot.blacklist:
                return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)

            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})

            interest = interests.split(" ")

            if len(interest) > 1:
                return await interaction.response.send_message("Please use only one word, as interest tag!", ephemeral=True)
            
            interest = interest[0]
            if len(data["interests"]) > 5:
                return await interaction.response.send_message("You can have max. 5 interests!", ephemeral=True)
            await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$push": {"interests": interest}})

            return await interaction.response.send_message(embed=discord.Embed(title=f"Interest added: {interest}", color=EMBED_COLOR), ephemeral=True)
        
    #@is_registered()
    @interest_group.command(name="remove", description="Remove a interest")
    async def interest_delete(self, interaction: discord.Interaction):
        """DELETE A INTEREST"""
        if await registered(self.bot, interaction.user):
            interests = await self.bot.db.find_one({"_id": str(interaction.user.id)})
            return await interaction.response.send_message(view=InterestSelectView(author=interaction.user, bot=self.bot, interests=interests["interests"]), ephemeral=True)

    #@is_registered()
    @app_commands.command(name="gender", description="Set your gender")
    async def profile_gender(self, interaction: discord.Interaction):
        """SET YOUR PROFILE GENDER"""
        if await registered(self.bot, interaction.user):
        
            return await interaction.response.send_message(view=SelectView(author=interaction.user, bot=self.bot), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Profile(bot))