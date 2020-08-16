import os
import discord
from miro import uploadWarmup
from markdown import markdownSheet
from cred import *
from commands import alias, loadAlias, commands
from util import *

client = discord.Client()

# https://leovoel.github.io/embed-visualizer/

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild:')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')


@client.event
async def on_message(message):
    channelId=message.channel.id
    message_text = message.content.strip()
    if message_text.startswith("/"):
        parts=message_text[1:].split(" ")
        cmd=parts[0]
        args=parts[1:]
        if channelId in alias and cmd in alias[channelId]:
            old_cmd=cmd
            cmd=alias[channelId][cmd]
            print("Found alias ",old_cmd,"=>",cmd)
        if cmd in commands:
            fun,_,_=commands[cmd]
            await fun(message,args)

loadAlias()
from commands import alias

client.run(BotToken)
