#!/usr/bin/python3

import discord
import json
import signal
import asyncio
from sb_commandcenter import *
import sb_command_funcs as funcs
from sb_command import Command
from sb_channelcommand import ChannelCommand
from sb_constants import *
from sb_db.accessor import DBAccessor
import json
import sb_db.errors as dberr
import time

from google.cloud import secretmanager

command_prefix = "8!"

if TEST_MODE:
    command_prefix = "7!"

secret_client = secretmanager.SecretManagerServiceClient()
path = secret_client.secret_version_path("discord-smashbot", "super_secret_smashbot_dev_config" if TEST_MODE else "super_secret_smashbot_prod_config", "latest")
response = secret_client.access_secret_version(request={"name": path})
NSA_IS_WATCHING = json.loads(response.payload.data.decode("utf-8"))

db_accessor = DBAccessor(NSA_IS_WATCHING["db_host"], NSA_IS_WATCHING["db_name"], NSA_IS_WATCHING["db_port"], NSA_IS_WATCHING["db_user"], NSA_IS_WATCHING["db_pass"])

intents = discord.Intents(messages=True, members=True, guilds=True, reactions=True, message_content=True)
client = discord.Client(intents=intents)

# Flag to track if we should shutdown
INTERRUPT_RECEIVED = False

def signal_handler(signum, frame):
    """Handle Ctrl+C signal to gracefully shutdown the bot"""
    global INTERRUPT_RECEIVED
    print("\nReceived Ctrl+C interrupt. Logging out gracefully...")
    INTERRUPT_RECEIVED = True
    if client.is_ready():
        asyncio.create_task(client.close())

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

command_center = CommandCenter(db_accessor, client)
command_center.register_command(Command(       "help",         funcs.help))
command_center.register_command(ChannelCommand("register",     funcs.register))
command_center.register_command(Command       ("update",       funcs.update))
command_center.register_command(ChannelCommand("playerlist",   funcs.player_list))
command_center.register_command(Command(       "profile",      funcs.profile))
command_center.register_command(ChannelCommand("whois",        funcs.profile))
command_center.register_command(Command(       "iplay",        funcs.i_play))
command_center.register_command(Command(       "remove",       funcs.i_dont_play))
command_center.register_command(Command(       "imain",        funcs.i_main))
command_center.register_command(Command(       "ipocket",      funcs.i_pocket))
command_center.register_command(ChannelCommand("whoplays",     funcs.who_plays))
command_center.register_command(Command(       "fighter",      funcs.fighter_info))
command_center.register_command(ChannelCommand("olimariscool", funcs.olimar_is_cool))
command_center.register_command(Command       ("coinflip",     funcs.coin_flip))
command_center.register_command(Command       ("saint",        funcs.saint))
command_center.register_command(ChannelCommand("hmu",          funcs.looking_for_match))
command_center.register_command(ChannelCommand("nothx",        funcs.not_looking_for_match))
command_center.register_command(ChannelCommand("letsplay",     funcs.ping_match_lookers))
# command_center.register_command(Command       ("ai",           funcs.ai_chat))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="{}help for commands".format(command_prefix)))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_disconnect():
    print("Bot has disconnected from Discord")

# Set up when joining a new guild
# This probably doesn't work currently since the bot
# won't have create role permissions when joining?
#@client.event
#async def on_guild_join(guild):
#    await guild.create_role(name="looking to smash", mentionable=True)

@client.event
async def on_message(message: discord.Message):
    channel = message.channel
    author = message.author

    if author == client.user:
        return

    if(not message.content.startswith(command_prefix)):
        return

    command_string = message.content[len(command_prefix):].strip()
    # override message content with sanitized input
    message.content = command_string
    command_name =  message.content.split(' ')[0]
    try:
        rc = await command_center.run_command(command_name, client, message)
    except dberr.DatabaseError:
        await channel.send("Commands that access the database are disabled because Rad doesn't want to spend money on a database right now.")
        return

    if(rc == RC_COMMAND_DNE):
        await channel.send("Command not recognized, {}".format(author.mention))
    elif(rc == RC_CHANNEL_ONLY):
        await channel.send("That command only works in channels.")


token = NSA_IS_WATCHING["discord_token"]

while not INTERRUPT_RECEIVED:
    try:
        client.run(token)
    except Exception as e:
        print(e)
        if not INTERRUPT_RECEIVED:
            time.sleep(3)
        else:
            break

print("Bot shutdown complete.")
