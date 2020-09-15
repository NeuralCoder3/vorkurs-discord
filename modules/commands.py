import discord
import datetime
from urllib.parse import quote_plus
import pickle
import os
from enum import Enum, auto
import git 
import datetime

try:
    from .util import *
    from .social import *
    from .cred import *
    from .miro import uploadWarmup
    from .markdown import markdownSheet, createFromFile
    from . import database as db
    from .reminder import remindme
    from . import scheduling as sched
except ImportError:
    from util import *
    from social import *
    from cred import *
    from miro import uploadWarmup
    from markdown import markdownSheet, createFromFile
    import database as db
    from reminder import remindme
    import scheduling as sched

class CommandGroup():
    def __init__(self,title="",key=None,hidden=False,color=0xadd8e6):
        self.key=key
        self.title=title
        self.hidden=hidden
        self.color=color

discordGroup=CommandGroup(title="Discord")
socialGroup=CommandGroup(title="PubQuiz",hidden=True,color=0xf9ffaf)
warmupGroup=CommandGroup(title="SLP",color=0xb7ffb2)
hiddenGroup=CommandGroup(hidden=True)
socialadminGroup=CommandGroup(hidden=True,key=socialkey)

g = git.cmd.Git(gitRepo)
dt = datetime.datetime.today()

datemap=[
    "A1","A2","A3","A4","A5","","",
    "B1","B2","B3","B4","B5","","",
    "C1","C2","C3","C4","C5","","",
    "D1","D2","D3","D4","D5","",""
]


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


async def help(message,args):
    global commands

    commandGroups=dict()
    for cmd in commands.keys():
        _,h,group=commands[cmd]
        if group.hidden:
            continue
        if group not in commandGroups:
            commandGroups[group]=[]
        commandGroups[group].append((cmd,h))
    for group,xs in commandGroups.items():
        if group.hidden:
            continue
        embedVar = discord.Embed(title=f"{group.title} Commands", description="", color=group.color)
        for cmd,h in xs:
            embedVar.add_field(name="/"+cmd, value=h, inline=False)
        await message.channel.send(embed=embedVar)

def replaceAlias(cmd,channelId):
    cursor=db.conn.cursor()
    q=list(cursor.execute("SELECT command FROM aliases WHERE alias=? AND channelID=?", (cmd,channelId)).fetchall())
    db.conn.commit()
    cursor.close()
    if len(q)>0:
        cmd=q[0][0]
    return cmd

def addAlias(message,args):
    if len(args)<2:
        return message.channel.send(f"wrong syntax.")
    channelId=message.channel.id
    aliasName=args[0]
    command=args[1]

    cursor=db.conn.cursor()
    cursor.execute("""REPLACE INTO 
    aliases(channelID,alias,command)
    VALUES (?,?,?)""",(channelId,aliasName,command))
    db.conn.commit()
    cursor.close()
    return message.channel.send(f"Alias {aliasName} for {command} was added in {message.channel}")
        
def listAlias(message,args):
    channelId=message.channel.id

    cursor=db.conn.cursor()
    aliasList=list(cursor.execute("SELECT alias,command FROM aliases WHERE channelID=?", (channelId,)).fetchall())
    db.conn.commit()
    cursor.close()
    if len(aliasList)>0:
        aliases=""
        for an,c in aliasList:
            aliases+=f"{an} ↦ {c}\n"
        return message.channel.send(aliases)
    else:
        return message.channel.send("No aliases found.")

def getCurrentTex():
    g.pull()
    idx=(dt.day+2)%30
    number=datemap[idx]
    sheetFile=sheetTex.replace(sheetPlaceholder,number)
    return sheetFile, number

async def createWarmupWhiteboard(channel):
    # url = uploadWarmup(testSheet1PDF,XXX)
    sheetFile,number=getCurrentTex()
    if number=="":
        print("It is a weekend")
        return
    pdf=compileTex(sheetFile)
    url = uploadWarmup(pdf,'o9J_knFi-8g=')
    # url = "TODO"
    print(f"Uploaded to {url}")
    await channel.send(f"Here is your warmup {url}")

async def createWarmupMarkdown(channel):
    sheetFile,number=getCurrentTex()
    if number=="":
        print("It is a weekend")
        return
    url = markdownSheet(sheetFile,number)
    print(f"Uploaded Markdown to {url}")
    await channel.send(f"Here is your markdown warmup {url}")

async def warmUpWhiteboard(message,args):
    await message.channel.send("Creating whiteboard.")
    await createWarmupWhiteboard(message.channel)

async def warmUpMarkdown(message,args):
    await message.channel.send("Creating markdown sheet.")
    await createWarmupMarkdown(message.channel)

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

async def reminder(message,args,here):
    if len(args)<1:
        await message.channel.send(f"wrong syntax.")
        return
    time=args[0]
    if len(args)>=2:
        msg=args[1]
    else:
        msg="Erinnerung!"
    await remindme(message,time,msg,here=here)

async def remindUs(message,args):
    await reminder(message,args,True)

async def remindMe(message,args):
    await reminder(message,args,False)

def scheduleWarmup(message,args):
    # if len(args)<1:
    hour=9
    min=30
    # else: # remove this
    #     parts=args[0].split(":")
    #     hour=int(parts[0])
    #     min=int(parts[1])
    channelId=message.channel.id
    sched.addTask(channelId,hour,min,"warmup")
    return message.channel.send(f"Subscription successful")

def scheduleWarmupMd(message,args):
    # if len(args)<1:
    hour=9
    min=30
    # else: # remove this
    #     parts=args[0].split(":")
    #     hour=int(parts[0])
    #     min=int(parts[1])
    channelId=message.channel.id
    sched.addTask(channelId,hour,min,"warmupmd")
    return message.channel.send(f"Subscription successful")

def scheduleDebug(message,args):
    parts=args[0].split(":")
    hour=int(parts[0])
    min=int(parts[1])
    channelId=message.channel.id
    sched.addTask(channelId,hour,min,"warmupmd")
    return message.channel.send(f"Subscription successful")

def unsubscribe(message,args):
    channelId=message.channel.id
    sched.removeAll(channelId)
    return message.channel.send(f"All subscriptions removed.")


commands={
    "links": (links,"Prints a list of useful links",warmupGroup),
    "warmup": (warmUpWhiteboard,"Creates a whiteboard with the current warm-up sheet",warmupGroup),
    "warmupMarkdown": (warmUpMarkdown,"Creates a markdown document with the current warm-up sheet",warmupGroup),
    "templateMarkdown": (templateMarkdown,"Creates a markdown document with some predefined aliases",warmupGroup),
    "help": (help,"Shows this help",discordGroup),
    "ask": (ask,"Asks the questions on the forum. Format /ask Title Text: Question",warmupGroup),
    "alias": (addAlias,"Adds an alias. Syntax: /alias newAlias cmd",discordGroup),
    "remindMe": (remindMe,"Sends a reminder after a specified time to you the user. Syntax: /remindMe time [message]",discordGroup),
    "remindUs": (remindUs,"Sends a reminder after a specified time to this channel. Syntax: /remindMe time [message]",discordGroup),
    "listAlias": (listAlias,"Lists all aliases in the channel",discordGroup),
    "subscribeWarmup": (scheduleWarmup,"Subscribe to daily warmup sheets.",warmupGroup),
    "subscribeWarmupMarkdown": (scheduleWarmup,"Subscribe to daily markdown warmup sheets.",warmupGroup),
    "subscribe": (scheduleDebug,"Subscribe debugging",hiddenGroup),
    "unsubscribe": (unsubscribe,"Removes all subscriptions.",warmupGroup),
    "nextGame": (nextGame,"Start next guessing game. syntax: nextGame key name",socialadminGroup),
    "showGame": (showGame,"Shows the answers. syntax: showGame key [name]",socialadminGroup),
    "guess": (guess,"Give a guess for the current game. syntax: guess answer",socialGroup),
}


