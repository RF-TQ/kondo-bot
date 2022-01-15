import os
from dotenv import load_dotenv
import discord
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import urllib.request, json
import time
import translations

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
    if message.author is None or message.author.roles is None:
        return
    if not "Mods" in [x.name for x in message.author.roles] and message.author.id != 148244502728015872:
        return

    message_parts = message.content.split(" ")
    command = message_parts[0]
    args = message_parts[1:]

    if command == "!rename":
        await message.channel.send("It's バランス time!")
        done = False
        users = await rename_all_users(message.guild)
        await message.channel.send("Kondo-ified {0} users.".format(users))

    if command == "!event":
        await update_event_timer(message.guild)
        await message.channel.send("Event timer updated.")

    if command == "!eventname":
        await update_event_timer(message.guild, set_tl=" ".join(args))

async def run_tasks():
    guild = client.get_guild(test_server_id)
    await update_event_timer(guild)
    await rename_all_users(guild)

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

async def update_event_timer(guild, set_tl=""):
    # Find event timers channel
    channel = get_channel(guild, "event-timers")
    # Delete old messages by the bot except for the last one
    last_message = None
    async for message in channel.history(limit=200):
        if message.author == client.user:
            if last_message is not None:
                await message.delete()
            last_message = message

    # Get event info
    with urllib.request.urlopen("https://sekai-world.github.io/sekai-master-db-diff/events.json") as url:
        events = json.loads(url.read().decode())
    # Get current event
    now_ms = time.time() * 1000
    newest_event = None
    day_ms = 1000 * 60 * 60 * 24
    for event in events:
        if now_ms > event["startAt"] - day_ms:
            newest_event = event
    # Get event properties
    start_time = event["startAt"]
    start_verb = "starts"
    if now_ms > start_time:
        start_verb = "started"
    end_time = event["aggregateAt"]
    end_verb = "ends"
    if now_ms > end_time:
        end_verb = "ended"
    event_name = newest_event["name"]
    event_name_tl = ""
    if len(set_tl) > 0:
        event_name_tl = set_tl
        translations.set(event_name, set_tl)
    else:
        event_name_tl = translations.get("en", event_name)
    start_sec = start_time // 1000
    end_sec = end_time // 1000
    logo_url = "https://sekai-res.dnaroma.eu/file/sekai-assets/event/{0}/logo_rip/logo.webp".format(newest_event["assetbundleName"])
    embed = discord.Embed()
    embed.set_image(url=logo_url)
    text = "The current event, **{0}**, {1} **<t:{2}:R>** on **<t:{3}:F>**.\n\nIt {4} **<t:{5}:R>** on **<t:{6}:F>**.".format(event_name_tl, start_verb, start_sec, start_sec, end_verb, end_sec, end_sec)
    if last_message is not None and text == last_message.content:
        return
    if last_message is not None:
        await last_message.delete()
    await channel.send(text, embed=embed)

def load_cron():
    sched = AsyncIOScheduler(timezone='EST')
    sched.start()
    sched.add_job(run_tasks, trigger='cron', minute=1)

def get_channel(guild, channel_name):
    for channel in guild.channels:
        if channel.name == channel_name:
            return channel

client.run(TOKEN)
