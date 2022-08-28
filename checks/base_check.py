import discord

class NotGuild(discord.app_commands.CheckFailure):
    pass

def is_owner(interaction:discord.Interaction):
    return interaction.user.id == 311450463553847299

def is_guild(interaction:discord.Interaction):
    if interaction.guild:
        return True
    raise NotGuild