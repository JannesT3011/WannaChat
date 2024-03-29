import discord
from discord.ext import commands
from discord import app_commands
from config import EMBED_COLOR
from better_profanity import profanity
from database.database import Database
from checks.base_check import is_guild
import asyncio
from utils import random_xp

class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    globalchat_group = app_commands.Group(name="globalchat", description="Start the global chat")

    @globalchat_group.command(name="activate", description="Activate the GlobalChat in this channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.bot_has_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def activate(self, interaction:discord.Interaction):
        """ACTIVATE GLOBAL CHAT IN CHANNEL"""

        globalchat_channels = await self.bot.gcserversdb.find_one({"_id": "servers"})

        if interaction.channel.id in globalchat_channels["channels"]:
            return await interaction.response.send_message("Channel already set!")
        
        await self.bot.gcserversdb.update_many({"_id": "servers"}, {"$push": {"channels": interaction.channel.id}})

        try:
            await interaction.channel.edit(topic="🌐💬 WannaChat Global chat, write message to different people all arount the world!", slowmode_delay=5)
        except discord.errors.Forbidden:
            pass

        return await interaction.response.send_message(embed=discord.Embed(title="This channel is now the GlobalChat channel!", description="You can now send messages to other servers or receive messages from them!", color=EMBED_COLOR))


    @globalchat_group.command(name="deactivate", description="Deactivate the GlobalChat in this channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def deactivate(self, interaction:discord.Interaction):
        """DEACTIVATE GLOABL CHAT IN CHANNEL"""
        try:
            await self.bot.gcserversdb.update_many({"_id": "servers"}, {"$pull": {"channels": interaction.channel.id}})
        except:
            return await interaction.response.send_message("No channel set, yet!")

        return await interaction.response.send_message(embed=discord.Embed(title="GlobalChat deactivated!"))

    @commands.Cog.listener()
    async def on_message(self, message): # TODO zu user db hinzufügen, wenn eine Message hinzugefügt wurde!
        if message.author.bot:
            return

        globalchat_data = await self.bot.gcserversdb.find_one({"_id": "servers"})
        #globalchat_channels = {"channels": [1000322624741703690, 566351183531343882]}

        if message.channel.id in globalchat_data["channels"]:
            try:
                await Database().init_db(str(message.author.id))
                await self.bot.queuedb.update_many({"_id": "queue"}, {"$push": {"queue": str(message.author.id)}})
                embed = discord.Embed(title="You can also use me to find new friends!", description="See `/help` for more infos.")
                await message.author.send(embed=embed)
            except:
                pass
            if message.author.id in globalchat_data["blacklist"]:
                return await message.author.send("You were banned from the GlobalChat!")

            globalchat_data["channels"].remove(message.channel.id)

            data = await self.bot.db.find_one({"_id": str(message.author.id)})
            old_xp = data["xp"]
            old_coins = data["coins"]
            
            await self.bot.db.update_many({"_id": str(message.author.id)}, {"$set": {"xp": old_xp + random_xp()}})
            await self.bot.db.update_many({"_id": str(message.author.id)}, {"$set": {"coins": old_coins + random_xp()}})

            for channel in globalchat_data["channels"]:
                try:
                    c = await self.bot.fetch_channel(channel)
                    embed = discord.Embed(
                        title=message.author.name, 
                        description=profanity.censor(message.content), 
                        timestamp=message.created_at, 
                        color=EMBED_COLOR if data["color"]=="" else discord.Colour.from_str(data["color"]))
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    await asyncio.sleep(0.5)
                    await c.send(embed=embed)
                except:
                    continue

async def setup(bot):
    await bot.add_cog(GlobalChat(bot))