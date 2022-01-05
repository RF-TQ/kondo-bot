import os
from dotenv import load_dotenv
import discord
import asyncio

# Load discord token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# When the bot is ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# When a message is received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == 319599477424128001:
        await message.channel.send("If you don't buy a G pack I'm making a 33 that's worse than Roku")
        return

    if not message.guild:
        await message.channel.send("Please buy more G packs to fund my yacht")
        return

    # Mod commands
    if not "Mods" in [x.name for x in message.author.roles] and message.author.id != 148244502728015872:
        return

    if message.content == "!rename":
        print("Renaming time")
        await message.channel.send("It's バランス time!")
        done = False
        users = await rename_all_users(message.guild)
        await message.channel.send("Kondo-ified {0} users.".format(users))

# Renames all users with nicknames starting with "!"
async def rename_all_users(guild):
    users = 0
    for i in range(len(guild.members)):
        user = guild.members[i]
        if (user.nick is None and user.name[0] == "!") or (not (user.nick is None) and user.nick[0] == "!"):
            users += 1
            await user.edit(nick="Hardcore Kondo Oshi")
    return users

client.run(TOKEN)
