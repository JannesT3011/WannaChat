import discord
from discord.ext import commands
import random
from discord.ui import Button, View
from config import PREFIX, EMBED_COLOR

class Tinder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_swiped = []


    async def add_to_likeduser(self, authorid, userid):
        """ADD USER TO LIKEDUSER DB""" 
        data = await self.bot.db.find_one({"_id": str(authorid)})
        if not str(userid) in data["liked_users"]:
            await self.bot.db.update_many({"_id": str(authorid)}, {"$push": {"liked_users":str(userid)}})
        #print(f"Added {userid} to {authorid}")


    async def add_to_likedby(self, likedbyid, userid):
        """ADD TO LIKEDBY DB"""
        data = await self.bot.db.find_one({"_id": str(userid)})
        if not str(likedbyid) in data["liked_by"]:
            await self.bot.db.update_many({"_id": str(userid)}, {"$push": {"liked_by": str(likedbyid)}})


    async def load_chatpartner(self, author, msg:any=None) -> str:
        """LOAD A NEW CHATPARTNER"""
        data = await self.bot.queuedb.find_one({"_id": "queue"})
        
        try:
            user_data = await self.bot.db.find_one({"_id": str(author.id)})
        except:
            return await author.send(f"Please use `{PREFIX}login` first")

        _queue = data["queue"]
        liked_users = user_data["liked_users"]
        likedby_users = user_data["liked_by"]

        queue = [user for user in _queue if user not in liked_users]
        queue = [user for user in queue if user not in self.already_swiped]

        if str(author.id) in queue:
            queue.remove(str(author.id))
        if len(queue) == 0:
            try:
                await msg.delete()
            except:
                pass
            return await author.send(f"Oh 😔, No more users! Please try again later!")

        chat_partner = random.choice(queue)
        
        while chat_partner == str(author.id):
            if len(queue) == 0:
                try:
                    await msg.delete()
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

        embed = discord.Embed(title=f"{chatpartner.name} 🧑", color=EMBED_COLOR)
        embed.add_field(name="Age", value=chat_partner_data["age"], inline=True)
        embed.add_field(name="Language", value=chat_partner_data["language"], inline=True)
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
        if str(authorid) in partner_data["liked_users"]:
            return True

        return False


    @commands.command(name='swipe', aliases=["match"]) # todo when swiping show users that has similar interests
    async def swipe(self, ctx):
        """SWIPE COMMAND"""
        self.already_swiped = []
        self.chat_partner_id = await self.load_chatpartner(ctx.author)
        self.chat_partner = self.bot.get_user(int(self.chat_partner_id))

        while self.chat_partner is None:
            self.chat_partner_id = await self.load_chatpartner(ctx.author)
            self.chat_partner = self.bot.get_user(int(self.chat_partner_id))

        embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)

        async def like_button_interaction(interaction):
            if await self.is_match(str(ctx.author.id), self.chat_partner_id):
                await ctx.author.send(embed=discord.Embed(title="🔥✨“ Yeah! New match! 🔥✨🔥", description=f"Match with {self.chat_partner.name}#{self.chat_partner.discriminator}", color=0x67ff90))
                try:
                    await self.chat_partner.send(embed=discord.Embed(title="🔥✨🔥 Yeah! New match! 🔥✨🔥", description=f"Match with {ctx.author.name}#{ctx.author.discriminator}", color=0x67ff90))
                except:
                    await ctx.author.send(embed=discord.Embed(title=f"Oh 😔, Cant contact your match! Please message first! 💬", color=EMBED_COLOR))
            
            await self.add_to_likedby(str(ctx.author.id), self.chat_partner_id)
            await self.add_to_likeduser(str(ctx.author.id), self.chat_partner_id)

            self.chat_partner_id = await self.load_chatpartner(ctx.author, msg=msg)
            self.chat_partner = self.bot.get_user(int(self.chat_partner_id))

            while self.chat_partner is None:
                self.chat_partner_id = await self.load_chatpartner(ctx.author)
                self.chat_partner = self.bot.get_user(int(self.chat_partner_id))

            embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)

            await interaction.response.edit_message(embed=embed) 


        async def dislike_button_interaction(interaction):
            try:
                self.chat_partner_id = await self.load_chatpartner(ctx.author, msg=msg)
                self.chat_partner = self.bot.get_user(int(self.chat_partner_id))

                while self.chat_partner is None:
                    self.chat_partner_id = await self.load_chatpartner(ctx.author)
                    self.chat_partner = self.bot.get_user(int(self.chat_partner_id))

                embed = await self.create_profile_embed(self.chat_partner, self.chat_partner_id)

                await interaction.response.edit_message(embed=embed) 
            except TypeError:
                like_button.disabled = True
                dislike_button.disabled = True

        like_button = Button(label="Like!", style=discord.ButtonStyle.green, emoji="❤️") 
        dislike_button = Button(label="Nah", style=discord.ButtonStyle.red, emoji="💤") # TODO error handler -> on_timeout -> delete message
        like_button.callback = like_button_interaction
        dislike_button.callback = dislike_button_interaction

        view = View()
        view.add_item(like_button)
        view.add_item(dislike_button)

        msg = await ctx.author.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Tinder(bot))