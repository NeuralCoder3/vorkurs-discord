import discord
import asyncio
import time

try:
    from .import database as db
    from .import commands as cmd
except ImportError:
    import database as db
    import commands as cmd

client=None

async def check_schedule():
    await client.wait_until_ready()
    # time.sleep(5)
    while True:

        tasks=checkTasks()
        for channelId, _, task in tasks:
            channel=client.get_channel(int(channelId))
            if task.lower()=="warmup":
                await cmd.createWarmupWhiteboard(channel)
            elif task.lower()=="warmupmd":
                await cmd.createWarmupMarkdown(channel)
            else:
                await channel.send("Doing "+task)
        # channelId=744652619506516198
        # await client.get_channel(channelId).send("Doing stuff")
        # print("Doing")

        await asyncio.sleep(5)

def addTask(channel,hour,min,task):
    # change 00:00 to now if not initial execution
    if hour>=2:
        hour-=2
    cursor=db.conn.cursor()
    cursor.execute("""REPLACE INTO 
    subscription(channelId,sched,executed,task)
    VALUES (?,?,datetime('00:00'),?)""",(channel,f"{hour:02d}:{min:02d}",task))
    db.conn.commit()
    cursor.close()

def checkTasks():
    cursor=db.conn.cursor()
    q=list(cursor.execute("""SELECT channelId, sched, task 
    FROM subscription WHERE
    strftime('%s', executed)-0 <
    strftime('%s', 'now','start of day')+(strftime('%s', sched)-strftime('%s', '00:00')) AND
    strftime('%s','now')-0>
    strftime('%s', 'now','start of day')+(strftime('%s', sched)-strftime('%s', '00:00'))
    """).fetchall())

    db.conn.commit()
    cursor.close()

    # print("task")
    # print(q)
    # print("All tasks")

    # cursor=db.conn.cursor()
    # q2=list(cursor.execute("""SELECT * FROM subscription """).fetchall())
    # db.conn.commit()
    # cursor.close()

    # print(q2)

    markDone(q)
    return q

def markDone(q):
    for gr in q:
        cursor=db.conn.cursor()
        cursor.execute("""UPDATE subscription
        SET executed=datetime('now')
        WHERE channelId=? AND sched=? AND task=?""",gr)
        db.conn.commit()
        cursor.close()