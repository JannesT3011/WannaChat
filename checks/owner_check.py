import discord

def is_owner(interaction:discord.Interaction):
    return interaction.user.id == 311450463553847299