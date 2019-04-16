#!/usr/bin/python3

import discord
import json
from sb_commandcenter import *
import sb_command_funcs as funcs
import mysql.connector
from sb_command import Command
from sb_channelcommand import ChannelCommand
from sb_constants import *

SECRET_CONFIG_FILE = './super_secret_config.json'

NSA_IS_WATCHING = {}

with open(SECRET_CONFIG_FILE) as json_file:  
    NSA_IS_WATCHING = json.load(json_file)

db = mysql.connector.connect(
  host="localhost",
  user=NSA_IS_WATCHING["db_user"],
  passwd=NSA_IS_WATCHING["db_pass"],
  database=NSA_IS_WATCHING["db_name"]
)

client = discord.Client()

command_center = CommandCenter()
command_center.register_command(Command("help", funcs.help))
command_center.register_command(ChannelCommand("register", funcs.register))
command_center.register_command(ChannelCommand("playerlist", funcs.player_list))
command_center.register_command(ChannelCommand("profile", funcs.profile))
command_center.register_command(ChannelCommand("whois", funcs.who_is))
command_center.register_command(ChannelCommand("olimariscool", funcs.olimar_is_cool))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Insert girder"))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    channel = message.channel
    author = message.author
    
    if author == client.user:
        return

    if(not message.content.startswith("8!")):
        return

    command_name = message.content.split(' ')[0][2:]
    rc = await command_center.run_command(command_name, client, message, db)

    if(rc == RC_COMMAND_DNE):
        await channel.send("Command not recognized, {}".format(author.mention))
    elif(rc == RC_CHANNEL_ONLY):
        await channel.send("That command only works in channels.")

client.run(NSA_IS_WATCHING["discord_token"])
