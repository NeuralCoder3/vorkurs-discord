import os
import discord


from modules.cred import *
import modules.cred as cred
# from modules.cred import *
from modules.util import *
from modules.miro import uploadWarmup
from modules.markdown import markdownSheet
from modules.commands import commands, replaceAlias
import modules.commands as cmds
import modules.database as db
import modules.scheduling as sched


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild:')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')


@client.event
async def on_message(message):
    channelId=message.channel.id
    # print(channelId)
    message_text = message.content.strip()
    if message_text.startswith("/"):
        parts=message_text[1:].split(" ")
        cmd=parts[0]
        args=parts[1:]
        cmd=replaceAlias(cmd,channelId)
        if cmd in commands:
            fun,_,group=commands[cmd]
            key=group.key
            if key is not None and key!="":
                if len(args)<1:
                    await message.channel.send("key expected")
                    return
                if args[0]!=key:
                    await message.channel.send("wrong key")
                    return
                args=args[1:]
            await fun(message,args)

database="/storage/data.db"
if not os.path.exists(database):
    print("use local database")
    database="."+database

db.create_connection(database)

sched.client=client
client.loop.create_task(sched.check_schedule())
client.run(BotToken)

