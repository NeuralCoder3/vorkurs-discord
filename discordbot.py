import os
import discord
from miro import uploadWarmup
from markdown import markdownSheet
from cred import BotToken
from cred import testSheet1PDF, testSheet1Tex

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild:')
    for guild in client.guilds:
        # if guild.name == GUILD:
        #     break

        print(f'{guild.name}(id: {guild.id})')

def cms(message):
    return message.channel.send("The cms is located at https://vorkurs.cs.uni-saarland.de/cms/ss20/")

def forum(message):
    return message.channel.send("The forum is located at https://vorkurs-discourse.cs.uni-saarland.de/")

def warmUpWhiteboard(message):
    url = uploadWarmup(testSheet1PDF)
    print(f"Uploaded to {url}")
    return message.channel.send(f"Here is your warmup {url}")

def warmUpMarkdown(message):
    url = markdownSheet(testSheet1Tex)
    print(f"Uploaded Markdown to {url}")
    return message.channel.send(f"Here is your markdown warmup {url}")

def help(message):
    global commands
    text="Following commands are available:\n"
    for cmd in commands.keys():
        _,h=commands[cmd]
        text+=f"/{cmd} \t {h}\n"
    return message.channel.send(text)

commands={
    "cms": (cms,"Prints the url of the CMS"),
    "forum": (forum,"Prints the url of the forum"),
    "warmup": (warmUpWhiteboard,"Creates a whiteboard with the current warm-up sheet"),
    "markdown": (warmUpMarkdown,"Creates a markdown document with the current warm-up sheet"),
    "help": (help,"Shows this help"),
}

@client.event
async def on_message(message):
    message_text = message.content.strip()
    for cmd in commands.keys():
        if message_text.lower().startswith("/"+cmd):
            fun,_=commands[cmd]
            await fun(message)
            break

client.run(BotToken)
