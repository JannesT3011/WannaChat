"""
UPDATE SWIPE TO PREVENT INTERACTION FAILED ERROR
"""
import discord
from discord.ext import commands
from discord import app_commands
import random
from discord.ui import Button, View
from config import PREFIX, EMBED_COLOR, TOPGG_TOKEN, LIMIT_LIKES
import topgg
from checks import is_registered
from utils import get_color, get_logger


logger = get_logger("Swipe2.0")

async def add_to_likeduser(bot, authorid, userid) -> None:
        """ADD SWIPED USER TO LIKED USER DB""" 
        data = await bot.db.find_one({"_id": str(authorid)})
        if not str(userid) in data["liked_users"]:
            await bot.db.update_many({"_id": str(authorid)}, {"$push": {"liked_users":str(userid)}})

async def add_to_disliked(bot, authorid, userid) -> None:
    """ADD SWIPED USER TO DISLIKED USER DB"""
    data = await bot.db.find_one({"_id": str(authorid)})
    if not str(userid) in data["disliked_users"]:
        await bot.db.update_many({"_id": str(authorid)}, {"$push": {"disliked_users":str(userid)}})

async def add_to_likedby(bot, likedbyid, userid) -> None:
    """ADD TO LIKEDBY DB"""
    data = await bot.db.find_one({"_id": str(userid)})
    if not str(likedbyid) in data["liked_by"]:
        await bot.db.update_many({"_id": str(userid)}, {"$push": {"liked_by": str(likedbyid)}})

async def is_match(bot, authorid, partnerid) -> bool:
    """CHECK IF MATCH"""
    partner_data = await bot.db.find_one({"_id": str(partnerid)})
    if str(authorid) in partner_data["liked_users"]: # TODO count matches!
        logger.info("New Match!")
        return True
    return False

class MatchView(discord.ui.View):
    def __init__(self, match_embed: discord.Embed):
        super(SwipeView, self).__init__(
            timeout=120
        )   

        self.match_embed = match_embed

        info_button = Button(label="Info", style=discord.ButtonStyle.grey, emoji="ℹ️")
        info_button.callback = self._info
        self.add_item(info_button)
    
    async def _info(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.match_embed, ephemeral=True)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        self.stop()

class SwipeView(discord.ui.View):
    def __init__(self, user):
        super(SwipeView, self).__init__(
            timeout=120
        )
        self.user = user
        self.interaction = None
        self.pressed = True

        like_button = Button(label="Like!", style=discord.ButtonStyle.green, emoji="❤️")
        like_button.callback = self._like
        self.add_item(like_button)

        dislike_button = Button(label="Nahh!", style=discord.ButtonStyle.blurple, emoji="❌") 
        dislike_button.callback = self._dislike
        self.add_item(dislike_button)
        
        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.grey, emoji="🛑")
        cancel_button.callback = self._cancel
        #self.add_item(cancel_button)
    

    async def _dislike(self, interaction: discord.Interaction):
        await add_to_disliked(interaction.client, str(interaction.user.id), self.chat_partner_id)
        self.interaction = interaction
        self.pressed = True
        self.stop()
    
    async def _like(self, interaction: discord.Interaction):
        if await is_match(interaction.client, str(interaction.user.id), self.chat_partner_id):
            #matchview = MatchView(self.partner_embed) # TODO geht noch nicht, weil funktin nicht zugreifbar!
            await interaction.response.send_message(embed=discord.Embed(title="🔥✨🔥 Yeah! New match! 🔥✨🔥", description=f"Match with: `{self.chat_partner.name}#{self.chat_partner.discriminator}`\n""➡️ Add your match and start chatting!\nDon't know how to start? Try: /starter", color=0x67ff90))
        
        await add_to_likedby(interaction.client, str(interaction.user.id), self.chat_partner_id)
        await add_to_likeduser(interaction.client, str(interaction.user.id), self.chat_partner_id)
        
        self.interaction = interaction
        self.pressed = True
        self.stop()
    

    async def _cancel(self, interaction: discord.Interaction):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

        self.interaction = interaction
        self.stop()

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
        self.stop()

class Swipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_swiped = []
        self.topgg = topgg.DBLClient(self.bot, TOPGG_TOKEN)
        self.match = ""
        self.match_id = ""

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
            return await author.send(f"Oh 😔, No more users! Please try again later!") # TODO return None here to stop interaction

        chat_partner = random.choice(queue)
        
        while chat_partner == str(author.id):
            if len(queue) == 0:
                try:
                    await interaction.response.edit_message(embed=discord.Embed(title="Click `dismiss message` to end"), view=None)
                except:
                    pass
                return await author.send(f"Oh 😔, No more users! Please try again later")  # TODO return None here to stop interaction
            
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
        return await self.swipe_backend(interaction)
    
    async def swipe_backend(self, interaction: discord.Interaction, edit:bool=False):
        try:
            data = await self.bot.db.find_one({"_id": str(interaction.user.id)})
        except:
            return

        if await self.on_swipelimit(data) and not await self.voted(int(interaction.user.id)):
            logger.debug("User on Swipelimit!")
            vote_button = Button(label="Vote vor me", url=f"https://top.gg/bot/{self.bot.user.id}/vote")
            view = View(timeout=None)
            view.add_item(vote_button)
            return await interaction.response.send_message(embed=discord.Embed(title="You reached the like limit!", description="Vote to get infinity likes!", color=EMBED_COLOR), view=view, ephemeral=True)
        
        view = SwipeView(interaction.user.id)

        #if not edit:
        #    await interaction.response.defer(thinking=True, ephemeral=True)

        try:
            self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
            self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
            # TODO check here if user is deleted
            view.chat_partner_id = self.chat_partner_id
            view.chat_partner = self.chat_partner
            
            while self.chat_partner is None:
                self.chat_partner_id = await self.load_chatpartner(interaction.user, interaction)
                self.chat_partner = await self.bot.fetch_user(int(self.chat_partner_id))
                view.chat_partner_id = self.chat_partner_id
                view.chat_partner = self.chat_partner

            embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)
            view.partner_embed = embed

        except TypeError:
            await view._cancel(interaction)

        if edit:
            await interaction.response.edit_message(embed=embed, view=view)
        
        else:
            await interaction.response.send_message(embed=embed, view=view)
        view.message = await interaction.original_response()
        await view.wait()
        interaction = view.interaction
        
        if view.pressed:
            return await self.swipe_backend(interaction, edit=True)
        
async def setup(bot):
    await bot.add_cog(Swipe(bot))