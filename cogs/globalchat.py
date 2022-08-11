import discord
from discord.ext import commands
from discord import app_commands
from config import EMBED_COLOR

class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    globalchat_group = app_commands.Group(name="globalchat", description="Start the global chat")

    @commands.bot_has_permissions(manage_guild=True)
    @commands.has_permissions(administrator=True)
    @globalchat_group.command(name="activate", description="Activate the GlobalChat in this channel")
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


    @commands.has_permissions(administrator=True)
    @globalchat_group.command(name="deactivate", description="Deactivate the GlobalChat in this channel")
    async def deactivate(self, interaction:discord.Interaction):
        """DEACTIVATE GLOABL CHAT IN CHANNEL"""
        try:
            await self.bot.gcserversdb.update_many({"_id": "servers"}, {"$pull": {"channels": interaction.channel.id}})
        except:
            return await interaction.response.send_message("No channel set, yet!")

        return await interaction.response.send_message(embed=discord.Embed(title="GlobalChat deactivated!"))
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        globalchat_channels = await self.bot.gcserversdb.find_one({"_id": "servers"})

        if message.channel.id in globalchat_channels["channels"]:
            if any(word in message.content for word in self.bot.blacklist):
                return await message.channel.send("Uh, dont use that word! 😞")

            globalchat_channels["channels"].remove(message.channel.id)

            for channel in globalchat_channels["channels"]:
                try:
                    c = await self.bot.fetch_channel(channel)
                    embed = discord.Embed(title=message.author.name, description=message.content, timestamp=message.created_at, color=message.author.color)
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    #embed.set_footer(icon_url=self.bot.user.display_avatar.url)
                    await c.send(embed=embed)
                except:
                    continue

async def setup(bot):
    await bot.add_cog(GlobalChat(bot))