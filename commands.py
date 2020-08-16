from cred import *
import discord
from miro import uploadWarmup
from markdown import markdownSheet, createFromFile
import datetime
from urllib.parse import quote_plus
from util import *
import pickle
import os

def links(message,args):
    embed = discord.Embed(title="Link-List", colour=discord.Colour(0x4a90e2), url="https://discordapp.com", description="Click the hyperreference for the concrete website.", timestamp=datetime.datetime.utcfromtimestamp(1597566031))

    embed.set_thumbnail(url="https://vorkurs.cs.uni-saarland.de/cms/ss20/theme/Vorkurs/img/logo.png")
    embed.set_author(name="Vorkurslinks", url="https://vorkurs.cs.uni-saarland.de/cms/ss20/", icon_url="https://vorkurs.cs.uni-saarland.de/cms/ss20/theme/Vorkurs/img/logo.png")
    embed.set_footer(text="aktuell am", icon_url="https://vorkurs.cs.uni-saarland.de/cms/ss20/theme/Vorkurs/img/logo.png")

    embed.add_field(name="CMS", value="[vorkurs.cs.uni-saarland](https://vorkurs.cs.uni-saarland.de/cms/ss20/)")
    embed.add_field(name="Forum", value="[vorkurs-discourse.cs.uni-saarland.de](https://vorkurs-discourse.cs.uni-saarland.de/)")
    embed.add_field(name="General-Whiteboard", value="[miro.com](https://miro.com/app/board/o9J_knFi-8g=/)")
    embed.add_field(name="Markdown-Help", value="[demo.codimd.org](https://demo.codimd.org/VS-PheYmRYudteqkamusjg?both)")
    embed.add_field(name="Gather.Town", value="[gather.town](https://gather.town/MKvrIqJweh6s7lpZ/CS)")
    embed.add_field(name="Games", value="TODO")

    return message.channel.send(embed=embed)

def help(message,args):
    global commands

    embedVar = discord.Embed(title="Commands", description="available commands", color=0xadd8e6)
    for cmd in commands.keys():
        _,h,show=commands[cmd]
        if show:
            embedVar.add_field(name="/"+cmd, value=h, inline=False)
    return message.channel.send(embed=embedVar)




def loadAlias():
    global alias
    if os.path.exists('alias.pickle'):
        with open('alias.pickle', 'rb') as f:
            alias=pickle.load(f)
            # print(alias)
    else:
        alias=dict()

def saveAlias():
    global alias
    with open('alias.pickle', 'wb') as f:
        pickle.dump(alias,f)
        # pickle.HIGHEST_PROTOCOL


channel2coaching=dict()
coaching2board=dict()

def warmUpWhiteboard(message,args):
    # url = uploadWarmup(testSheet1PDF,XXX)
    pdf=compileTex(testSheet1Tex)
    url = uploadWarmup(pdf,'o9J_knFi-8g=')
    # url = "TODO"
    print(f"Uploaded to {url}")
    return message.channel.send(f"Here is your warmup {url}")

def warmUpMarkdown(message,args):
    url = markdownSheet(testSheet1Tex)
    print(f"Uploaded Markdown to {url}")
    return message.channel.send(f"Here is your markdown warmup {url}")

def templateMarkdown(message,args):
    url=createFromFile("markdownHeader.md")
    return message.channel.send(f"Here is your markdown document {url}")

def ask(message,args):
    text=" ".join(args)
    parts=text.split(":")
    if len(parts)>1:
        title=quote_plus(parts[0])
        body=quote_plus(":".join(parts[1:]))
        url = f"https://vorkurs-discourse.cs.uni-saarland.de/new-topic?title={title}&body={body}&category_id=16&tags=discord"
        return message.channel.send(f"Follow this link {url}. You maybe have to change the category.")
    else:
        return message.channel.send(f"wrong syntax.")

def addAlias(message,args):
    if len(args)<2:
        return message.channel.send(f"wrong syntax.")
    global alias
    channelId=message.channel.id
    aliasName=args[0]
    command=args[1]
    if not channelId in alias:
        alias[channelId]=dict()
    alias[channelId][aliasName]=command
    # alias[(channelId,aliasName)]=command
    saveAlias()
    return message.channel.send(f"Alias {aliasName} for {command} was added in {message.channel}")
        
def listAlias(message,args):
    global alias
    channelId=message.channel.id
    aliasList=""
    if not channelId in alias:
        return message.channel.send("No aliases found.")
    for an,c in alias[channelId].items():
        aliasList+=f"{an} ↦ {c}\n"
    # for k,c in alias.items():
    #     ci,an = k
    #     if ci==channelId:
    #         aliasList+=f"{an} ↦ {c}\n"
    return message.channel.send(aliasList)


# @ bot.command()
async def createCoach(message,args):
    if len(args)<1:
        await message.channel.send("wrong syntax")
        return
    name=args[0] # Coaching #1
    role=await message.guild.create_role(name=name)
    overwrites = {
        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True)
    }

    cat=await message.guild.create_category(name, overwrites=overwrites)
    await message.guild.create_text_channel(name,category=cat, overwrites=overwrites)
    await message.guild.create_voice_channel(name,category=cat, overwrites=overwrites)

        
commands={
    "links": (links,"Prints a list of useful links",True),
    "warmup": (warmUpWhiteboard,"Creates a whiteboard with the current warm-up sheet",True),
    "warmupMarkdown": (warmUpMarkdown,"Creates a markdown document with the current warm-up sheet",True),
    "templateMarkdown": (templateMarkdown,"Creates a markdown document with some predefined aliases",True),
    "help": (help,"Shows this help",True),
    "ask": (ask,"Asks the questions on the forum. Format /ask Title Text: Question",True),
    "alias": (addAlias,"Adds an alias. Syntax: /alias newAlias cmd",True),
    "listAlias": (listAlias,"Lists all aliases in the channel",True),

    "createCoaching": (createCoach,"",False),
}

alias=dict()