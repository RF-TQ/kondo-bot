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
        print(message.content)
        await message.channel.send("Please buy more G packs to fund my yacht")
        return

    await message.channel.send("Hey, it's me, Kondo!")

client.run(TOKEN)
