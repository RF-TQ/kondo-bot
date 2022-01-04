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

    if not message.guild:
        await message.channel.send("Please buy more G packs to fund my yacht")
        return

    # Mod commands
    if not "Mods" in [x.name for x in message.author.roles]:
        return

    if message.content == "!rename":
        print("Renaming time")
        done = False
        users = 0
        while not done:
            done, new_users = await rename_users(message.guild)
            users += new_users
        await message.channel.send("Kondo-ified {0} users.".format(users))

# Renames all users with nicknames starting with "!"
async def rename_users(guild):
    users = await guild.query_members("!", limit=100)
    if len(users) == 0:
        return True
    print(users)
    for i in range(len(users)):
        user = users[i]
        print(user)
        await user.edit(nick="Hardcore Kondo Oshi")
    return False, len(users)

client.run(TOKEN)
