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
        await rename_users(message.guild)

# Renames all users with nicknames starting with "!"
async def rename_users(guild):
    users = await guild.query_members("!")
    for i in range(len(users)):
        user = users[i]
        await user.edit(nick="Hardcore Kondo Oshi")

client.run(TOKEN)
