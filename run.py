import os
from dotenv import load_dotenv
import discord
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sekaicord_id = 636538718387306528
test_server_id = 907674756684333187

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
    load_cron()

# When a message is received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.guild:
        if message.author.id == 319599477424128001:
            await message.channel.send("If you don't buy a G pack I'm making a 33 that's worse than Roku")
            return
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
        banned = ["!", "#"]
        if (user.nick is None and user.name[0] in banned) or (not (user.nick is None) and user.nick[0] in banned):
            users += 1
            await user.edit(nick="Hardcore Kondo Oshi")
    return users

async def rename_all():
    guild = client.get_guild(sekaicord_id)
    await rename_all_users(guild)

def load_cron():
    sched = AsyncIOScheduler(timezone='EST')
    sched.start()
    sched.add_job(rename_all, trigger='cron', minute=15)

client.run(TOKEN)
