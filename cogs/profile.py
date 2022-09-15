import discord
from discord.ext import commands
from discord import app_commands
from config import PREFIX, EMBED_COLOR
from checks.registered import is_registered
from checks.voted import is_voter
from matplotlib.colors import is_color_like


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

    async def on_timeout(self) -> None:
        self.stop()

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

    @app_commands.command(name="profile", description="View your profile")
    @is_registered()
    async def profile(self, interaction: discord.Interaction):
        """VIEW PROFILE"""
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})

        embed = discord.Embed(title="Your profile 🧑", color=EMBED_COLOR if data["color"]=="" else discord.Colour.from_str(data["color"]))
        embed.add_field(name="Age", value=data["age"], inline=True)
        embed.add_field(name="Language", value=", ".join(data["language"]), inline=True)
        embed.add_field(name="Gender", value=data["gender"])

        if not len(data["interests"]) == 0:
            embed.add_field(name="Interests", value=", ".join(data['interests']), inline=False)
        if not data["aboutme"] == "":
            embed.add_field(name="About me", value=data["aboutme"], inline=False)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"See how you modify your profile with {PREFIX}help")

        await interaction.response.defer(ephemeral=True, thinking=True)
        if data:
            await interaction.followup.send(embed=embed, view=SelectView(author=interaction.user, bot=self.bot), ephemeral=True)
        
        embed = discord.Embed(title="Complete your profile:", color=EMBED_COLOR)
        if data["gender"] == "-":
            embed.add_field(name="❌ Add your gender:", value=f"`{PREFIX}gender`", inline=False)
        if data["age"] == "-":
            embed.add_field(name="❌ Add your age:", value=f"`{PREFIX}age`", inline=False)
        if len(data["interests"]) == 0:
            embed.add_field(name="❌ Add some interests:", value=f"`{PREFIX}interests add`", inline=False)
        if data["aboutme"] == "":
            embed.add_field(name="❌ Write something about yourself:", value=f"`{PREFIX}aboutme`", inline=False)
        if len(embed.fields) == 0:
            return

        return await interaction.user.send(embed=embed)
        
    @app_commands.command(name="age", description="Set your age")
    @is_registered()
    async def profile_age(self, interaction: discord.Interaction, age:int):
        """SET YOUR PROFILE AGE"""
        if age in self.bot.blacklist:
            return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)
        if age > 119:
            return await interaction.response.send_message("I dont think the oldest person on this world is using this Bot 👵. But if you are, send me a message with: `wc.bug`")
        try:
            r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"age": age}})
        except:
            return await interaction.response.send_message(f"Please use `{PREFIX}login` first", ephemeral=True)
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if r:
            return await interaction.followup.send(embed=discord.Embed(title=f"Age set to {age}",color=EMBED_COLOR), ephemeral=True)
        
    @profile_age.error
    async def age_error(self, interaction: discord.Interaction, error):
        """AGE ERROR HANDLER"""
        if isinstance(error, commands.BadArgument):
            return await interaction.response.send_message("Urgg, Thats not a number...", ephemeral=True)

    language_group = app_commands.Group(name="language", description="See, add or remove your languages")

    @language_group.command(name="view", description="See your current languages") 
    @is_registered()
    async def language(self, interaction: discord.Interaction):
        """SET YOUR PROFILE LANGUAGE"""
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if data:
            return await interaction.followup.send(embed=discord.Embed(title="Your current languages:", description=", ".join(data["language"])).set_footer(text=f"Use: {PREFIX}language <add/delete> to add/delete a language"), ephemeral=True)
        
    @language_group.command(name="add", description="Add one language")
    @is_registered()
    async def language_add(self, interaction: discord.Interaction, language:str):
        if language in self.bot.blacklist:
            return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        
        if len(data["language"]) > 5:
            return await interaction.response.send_message("You can have max. 5 languages!")
        
        if language in data["language"]:
            return await interaction.response.send_message("Language already added!")
        await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$push": {"language": language.lower()}})
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if data:
            return await interaction.followup.send(embed=discord.Embed(title=f"Language added: {language}", color=EMBED_COLOR), ephemeral=True)
        
    @language_group.command(name="remove", description="Remove a language")
    @is_registered()
    async def language_delete(self, interaction: discord.Interaction):
        languages = await self.bot.db.find_one({"_id": str(interaction.user.id)})

        await interaction.response.defer(ephemeral=True, thinking=True)
        if languages:
            return await interaction.followup.send(view=LanguageSelectView(author=interaction.user, bot=self.bot, language=languages["language"]), ephemeral=True)

    @app_commands.command(name="aboutme", description="Set your AboutMe description")
    @is_registered()
    async def profile_aboutme(self, interaction: discord.Interaction, *, aboutme:str):
        """SET YOUR PROFILE ABOUTME"""
        if len(aboutme) == 100:
            return await interaction.response.send_message("Aboutme can only be 100 characters long", ephemeral=True)
        if any(word in aboutme for word in self.bot.blacklist):
            return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)
        try:
            r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"aboutme": aboutme}})
        except:
            return await interaction.response.send_message(f"Please use `{PREFIX}login` first", ephemeral=True)
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if r:
            return await interaction.followup.send(embed=discord.Embed(title=f"Aboutme set to `{aboutme}`", color=EMBED_COLOR), ephemeral=True)
        
    interest_group = app_commands.Group(name="interests", description="View, add and remove your interests")

    @interest_group.command(name="view", description="See your interests")
    @is_registered()
    async def interests(self, interaction: discord.Interaction):
        """SET YOUR PROFILE INTERESTS"""
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        if data:
            return await interaction.followup.send(embed=discord.Embed(title="Your current interests:", description=", ".join(data["interests"])).set_footer(text=f"Use: {PREFIX}interests <add/delete> to add/delete a interests"), ephemeral=True)
        
    @interest_group.command(name="add", description="Add a interest")
    @is_registered()
    async def interest_add(self, interaction: discord.Interaction, *, interests:str):
        """ADD INTEREST"""
        if interests in self.bot.blacklist:
            return await interaction.response.send_message("Uh, dont use that word! 😞", ephemeral=True)
        interest = interests.split(" ")
        if len(interest) > 1:
            return await interaction.response.send_message("Please use only one word, as interest tag!", ephemeral=True)
        
        interest = interest[0]
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        if len(data["interests"]) > 5:
            return await interaction.response.send_message("You can have max. 5 interests!", ephemeral=True)
        await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$push": {"interests": interest}})
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if data:
            return await interaction.followup.send(embed=discord.Embed(title=f"Interest added: {interest}", color=EMBED_COLOR), ephemeral=True)
        
    @interest_group.command(name="remove", description="Remove a interest")
    @is_registered()
    async def interest_delete(self, interaction: discord.Interaction):
        """DELETE A INTEREST"""
        interests = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if interests:
            return await interaction.followup.send(view=InterestSelectView(author=interaction.user, bot=self.bot, interests=interests["interests"]), ephemeral=True)

    @app_commands.command(name="gender", description="Set your gender")
    @is_registered()
    async def profile_gender(self, interaction: discord.Interaction):
        """SET YOUR PROFILE GENDER"""
        return await interaction.response.send_message(view=SelectView(author=interaction.user, bot=self.bot), ephemeral=True)

    @app_commands.command(name="color", description="Set your profile color")
    @is_registered()
    @is_voter()
    async def profile_color(self, interaction: discord.Interaction, color: str):
        if not is_color_like(color) and not color.startswith("#"):
            return await interaction.response.send_message("please provide a valid color!", ephemeral=True)
        r = await self.bot.db.update_many({"_id": str(interaction.user.id)}, {"$set": {"color": color}})
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if r:
            return await interaction.followup.send(embed=discord.Embed(title=f"Profile color set to: {color}"))

async def setup(bot):
    await bot.add_cog(Profile(bot))