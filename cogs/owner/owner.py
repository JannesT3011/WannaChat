import discord
from discord.ext import commands, tasks
from discord import app_commands
from checks import is_owner
from typing import Literal
from database.database import Database

TEST_GUILD = discord.Object(364335676549890048)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remove_deleted_users_task.start()

    @app_commands.command(name='users', description="Get the total users")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def users(self, interaction: discord.Interaction):
        """GET THE AMOUNT OF BOT USERS"""
        data = await self.bot.queuedb.find_one({"_id": "queue"})

        return await interaction.response.send_message(f"We are currently {len(data['queue'])} users", ephemeral=True)
    
    @app_commands.command(name="servers", description="Get the server count")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def guilds(self, interaction: discord.Interaction):
        """GET THE AMOUNT OF BOT GUILDS"""
        return await interaction.response.send_message(f"Im currenty on {len(self.bot.guilds)} server(s)", ephemeral=True)
    
    @app_commands.command(name="status", description="Change the status of the Bot")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def status(self, interaction: discord.Interaction, type:Literal["game", "watching", "listening"], game:str):
        """SET THE BOT STATUS"""
        if type == "game":
            await self.bot.change_presence(activity=discord.Game(name=game))
        elif type == "watching":
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=game))
        elif type == "listening":
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=game))
        else:
            return await interaction.response.send_message("No valid type -> `game, watching, listening`")

        return await interaction.response.send_message(f"Status set to {game}", ephemeral=True)
    
    @app_commands.command(name="stats", description="Stats about the bot")
    #@app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def _stats(self, interaction: discord.Interaction):
        """SHOW USERS AND SERVERS IN ONE MESSAGE"""
        await interaction.response.defer(thinking=True)
        data = await self.bot.queuedb.find_one({"_id": "queue"})

        if data:
            return await interaction.followup.send(embed=discord.Embed(title="Stats", description=f"**Servers:** {len(self.bot.guilds)}\n**Users:** {len(data['queue'])}\n", timestamp=interaction.created_at), ephemeral=True)
    
    @app_commands.command(name="delete_users", description="Delete all non existing users")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def delete_users(self, interaction: discord.Interaction):
        await interaction.response.send_message("Remove all deleted users!", ephemeral=True)
        del_users = await self.remove_deleted_users()

        return await interaction.user.send(f"Done! Deleted {len(del_users)} users!", ephemeral=True)


    @app_commands.command(name="gcban", description="Ban user from GlobalChat")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.check(is_owner)
    async def gcban(self, interaction: discord.Interaction, user:int):
        await self.bot.gcserversdb.update_many({"_id": "servers"}, {"$push": {"blacklist": user}})

        try:
            user = await self.bot.fetch_user(user)
        except:
            return await interaction.response.send_message(embed=discord.Embed(title=f"{user} banned!"))

        globalchat_data = await self.bot.gcserversdb.find_one({"_id": "servers"})

        for channel in globalchat_data["channels"]:
            try:
                c = await self.bot.fetch_channel(channel)
                embed = discord.Embed(title=f"{user.name} banned!")
                embed.set_thumbnail(url=user.display_avatar.url)
                await c.send(embed=embed)
            except:
                continue

        return await interaction.response.send_message(embed=discord.Embed(title=f"{user.name} banned!"), ephemeral=True)

    @tasks.loop(hours=24)
    async def remove_deleted_users_task(self):
        del_users = await self.remove_deleted_users()
        print(f"Remove {del_users} users!")

    async def remove_deleted_users(self) -> list:
        deleted = []
        uids = await self.bot.db.distinct("_id")
        for id in uids:
            user = await self.bot.fetch_user(int(id))
            if user.name.startswith("Deleted User"):
                await Database().delete_db(str(user.id))
                await self.bot.queuedb.update_many({"_id": "queue"}, {"$pull": {"queue": str(user.id)}})
                print(f"Remove {user.name}, {user.id}")
                deleted.append(id)
        return deleted


async def setup(bot):
    await bot.add_cog(Owner(bot))