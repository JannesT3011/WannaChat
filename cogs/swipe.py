import discord
from discord.ext import commands
from discord import app_commands
import random
from discord.ui import Button, View
from config import PREFIX, EMBED_COLOR, TOPGG_TOKEN, LIMIT_LIKES
import topgg
from checks import is_registered
from utils import get_color, get_logger

logger = get_logger("Swipe")

class Swipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_swiped = []
        self.topgg = topgg.DBLClient(self.bot, TOPGG_TOKEN)
        self.match = ""
        self.match_id = ""

    async def add_to_likeduser(self, authorid, userid) -> None:
        """ADD SWIPED USER TO LIKED USER DB""" 
        data = await self.bot.db.find_one({"_id": str(authorid)})
        if not str(userid) in data["liked_users"]:
            await self.bot.db.update_many({"_id": str(authorid)}, {"$push": {"liked_users":str(userid)}})

    async def add_to_disliked(self, authorid, userid) -> None:
        """ADD SWIPED USER TO DISLIKED USER DB"""
        data = await self.bot.db.find_one({"_id": str(authorid)})
        if not str(userid) in data["disliked_users"]:
            await self.bot.db.update_many({"_id": str(authorid)}, {"$push": {"disliked_users":str(userid)}})

    async def add_to_likedby(self, likedbyid, userid) -> None:
        """ADD TO LIKEDBY DB"""
        data = await self.bot.db.find_one({"_id": str(userid)})
        if not str(likedbyid) in data["liked_by"]:
            await self.bot.db.update_many({"_id": str(userid)}, {"$push": {"liked_by": str(likedbyid)}})

    async def submit_report(self, authorid, userid):
        return
    
    async def needs_to_delete() -> bool:
        return

    async def load_chatpartner(self, author, interaction: discord.Interaction):
        """LOAD A NEW CHATPARTNER"""
        data = await self.bot.queuedb.find_one({"_id": "queue"})
        
        user_data = await self.bot.db.find_one({"_id": str(author.id)})

        _queue = data["queue"]
        liked_users = user_data["liked_users"]
        likedby_users = user_data["liked_by"]
        disliked_users = user_data["disliked_users"]

        queue = [user for user in _queue if user not in liked_users]
        queue = [user for user in queue if user not in self.already_swiped]
        queue = [user for user in queue if user not in disliked_users]

        if str(author.id) in queue:
            queue.remove(str(author.id))
        if len(queue) == 0:
            try:
                await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)
            except:
                pass
            return await author.send(f"Oh 😔, No more users! Please try again later!")

        chat_partner = random.choice(queue)
        
        while chat_partner == str(author.id):
            if len(queue) == 0:
                try:
                    await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)
                except:
                    pass
                return await author.send(f"Oh 😔, No more users! Please try again later")
            
            if len(likedby_users) >= 1:
                if random.randint(1,2) == 1:
                    chat_partner = random.choice(queue)
                else:
                    chat_partner = random.choice(likedby_users)
                    if chat_partner in self.already_swiped:
                        chat_partner = random.choice(queue)
            else:
                chat_partner = random.choice(queue)

        self.already_swiped.append(chat_partner) 
        
        return chat_partner


    async def create_profile_embed(self, chatpartner, chatpartner_id) -> discord.Embed:
        """CREATE THE PROFILE EMBED"""
        chat_partner_data = await self.bot.db.find_one({"_id": str(chatpartner_id)})

        embed = discord.Embed(title=f"{chatpartner.name} 🧑", color=await get_color(self.bot.db, chatpartner_id))
        embed.add_field(name="Age", value=chat_partner_data["age"], inline=True)
        embed.add_field(name="Language", value=", ".join(chat_partner_data["language"]), inline=True)
        embed.add_field(name="Gender", value=chat_partner_data["gender"])
        if not len(chat_partner_data["interests"]) == 0:
            embed.add_field(name="Interests", value=", ".join(chat_partner_data['interests']), inline=False)
        if not chat_partner_data["aboutme"] == "":
            embed.add_field(name="About me", value=chat_partner_data["aboutme"], inline=False)
        embed.set_thumbnail(url=chatpartner.display_avatar.url)

        return embed


    async def is_match(self, authorid, partnerid) -> bool:
        """CHECK IF MATCH"""
        partner_data = await self.bot.db.find_one({"_id": str(partnerid)})
        if str(authorid) in partner_data["liked_users"]: # TODO count matches!
            logger.info("New Match!")
            return True

        return False

    async def on_swipelimit(self, data) -> bool:
        """CHECK IF USER ON SWIPELIMIT"""
        if len(data["liked_users"]) > LIMIT_LIKES:
            return True
        return False

    async def voted(self, userid:int) -> bool: # TODO Check if in voting list!
        """CHECK IF USER VOTED"""
        topgg_client = topgg.DBLClient(self.bot, TOPGG_TOKEN)
        check = await topgg_client.get_user_vote(userid)
        await topgg_client.close()
        
        return check

    @app_commands.command(name="swipe", description="Start swiping and find a random chat partner")
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    @is_registered()
    async def swipe(self, interaction: discord.Interaction):
        """SWIPE COMMAND"""
        self.already_swiped = []
        self.match = ""
        self.match_id = ""
        data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        
        if await self.on_swipelimit(data) and not await self.voted(int(interaction.user.id)):
            logger.debug("User on Swipelimit!")
            vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{self.bot.user.id}/vote")
            view = View(timeout=None)
            view.add_item(vote_button)
            return await interaction.response.send_message(embed=discord.Embed(title="You reached the like limit!", description="Vote to get infinity likes!", color=EMBED_COLOR), view=view, ephemeral=True)
        
        self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
        self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
        
        while self.chat_partner is None:
            self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
            self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
        
        embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)
        
        async def info_button_interaction(interacion: discord.Interaction):
            embed = await self.create_profile_embed(self.match, self.match_id)
            await interacion.response.send_message(embed=embed, ephemeral=True)
        
        async def like_button_interaction(interaction: discord.Interaction):
            if await self.is_match(str(interaction.user.id), self.chat_partner_id):
                self.match = self.chat_partner
                self.match_id = self.chat_partner_id
                info_button = Button(label="Info", style=discord.ButtonStyle.grey, emoji="ℹ️")
                info_button.callback = info_button_interaction
                view = View()
                view.add_item(info_button)
                await interaction.response.send_message(embed=discord.Embed(title="🔥✨🔥 Yeah! New match! 🔥✨🔥", description=f"Match with: `{self.chat_partner.name}#{self.chat_partner.discriminator}`\n""➡️ Add your match and start chatting!", color=0x67ff90), view=view)
                try:
                    await self.chat_partner.send(embed=discord.Embed(title="🔥✨🔥 Yeah! New match! 🔥✨🔥", description=f"Match with: `{interaction.user.name}#{interaction.user.discriminator}`\n""➡️ Add your match and start chatting!", color=0x67ff90), view=view)
                except:
                    await interaction.response.send_message(embed=discord.Embed(title=f"Oh 😔, Cant contact your match! Please message first! 💬", color=EMBED_COLOR), ephemeral=True)
            
            await self.add_to_likedby(str(interaction.user.id), self.chat_partner_id)
            await self.add_to_likeduser(str(interaction.user.id), self.chat_partner_id)
            
            self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
            self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
            
            while self.chat_partner is None:
                self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
                self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
           
            embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)

            if embed:
                await interaction.response.edit_message(embed=embed) 
        
        async def dislike_button_interaction(interaction: discord.Interaction):
            await self.add_to_disliked(str(interaction.user.id), self.chat_partner_id)
            try:
                self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
                self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
                
                while self.chat_partner is None:
                    self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
                    self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
                
                embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)

                if embed:
                    await interaction.response.edit_message(embed=embed) 

            except TypeError:
                like_button.disabled = True
                dislike_button.disabled = True
            
        async def cancel_button_interaction(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)
        
        like_button = Button(label="Like!", style=discord.ButtonStyle.green, emoji="❤️") 
        dislike_button = Button(label="Nah", style=discord.ButtonStyle.red, emoji="💤") # TODO error handler -> on_timeout -> await interaction.delete_original_message() message
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.grey, emoji="❌")
        like_button.callback = like_button_interaction
        dislike_button.callback = dislike_button_interaction
        cancel_button.callback = cancel_button_interaction
       
        view = View()
        #await view.wait()
        view.add_item(like_button)
        view.add_item(dislike_button)
        view.add_item(cancel_button)
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        if embed:
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        
        author_data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        embed = discord.Embed(title="Please complete your profile:", color=EMBED_COLOR)
        
        if author_data["gender"] == "-":
            embed.add_field(name="❌ Add your gender:", value=f"`{PREFIX}gender`", inline=False)
        if author_data["age"] == "-":
            embed.add_field(name="❌ Add your age:", value=f"`{PREFIX}age`", inline=False)
        if len(author_data["interests"]) == 0:
            embed.add_field(name="❌ Add some interests:", value=f"`{PREFIX}interests add`", inline=False)
        if author_data["aboutme"] == "":
            embed.add_field(name="❌ Write something about yourself:", value=f"`{PREFIX}aboutme`", inline=False)
        if len(embed.fields) == 0:
            return
        try:
            await interaction.user.send(embed=embed)
        except:
            logger.debug("Cant send message to this user")
            return

async def setup(bot):
    await bot.add_cog(Swipe(bot))