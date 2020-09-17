import sqlite3
from sqlite3 import Error

try:
    from .cred import boardFile
except ImportError:
    from cred import boardFile

conn=None

def create_connection(db_file):
    global conn
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("""
CREATE TABLE IF NOT EXISTS aliases (
    alias TEXT NOT NULL,
    channelID TEXT NOT NULL,
    command TEXT NOT NULL,
    PRIMARY KEY (alias,channelID)
);""")
        conn.commit()
        conn.execute("""
CREATE TABLE IF NOT EXISTS cache (
    file TEXT NOT NULL PRIMARY KEY,
    url TEXT NOT NULL,
    time DATETIME
);""")
        conn.commit()
        conn.execute("""
CREATE TABLE IF NOT EXISTS subscription (
    channelId TEXT NOT NULL,
    sched TEXT,
    executed DATETIME,
    task TEXT,
    PRIMARY KEY (channelId, sched,task)
);""")
        conn.commit()
        conn.execute("""
CREATE TABLE IF NOT EXISTS claims (
    boardUrl TEXT NOT NULL,
    channelId TEXT DEFAULT NULL,
    PRIMARY KEY (boardUrl),
    UNIQUE(boardUrl,channelId)
);""")
        conn.commit()
        tryInsertBoards()
    except Error as e:
        print(e)
    return conn

def findBoardListFromId(channelId,cursor):
    q=list(cursor.execute("SELECT boardUrl FROM claims WHERE channelId=?", (channelId,)).fetchall())
    conn.commit()
    return q

def getBoardUrl(channelId):
    cursor=conn.cursor()

    q=findBoardListFromId(channelId,cursor)

    if len(q)==0:
        print("claim a new board")
        cursor.execute("UPDATE claims SET channelId=? WHERE boardUrl in (SELECT boardUrl FROM claims WHERE channelId IS NULL LIMIT 1)", (channelId,))
        conn.commit()
        q=findBoardListFromId(channelId,cursor)

    cursor.close()

    if len(q)==0:
        return "No board for you!"
    else:
        return q[0][0]


def tryInsertBoards():
    boards=open(boardFile).readlines()
    boards=filter(lambda s: "http" in s, boards)

    cursor=conn.cursor()
    for boardUrl in boards:
        boardUrl=boardUrl.strip()
        cursor.execute("INSERT OR IGNORE INTO claims(boardUrl) VALUES(?)", (boardUrl,))
        conn.commit()

    cursor.close()

def lookupCache(file):
    cursor=conn.cursor()
    q=list(cursor.execute("SELECT url FROM cache WHERE file=?", (file,)).fetchall())
    conn.commit()
    cursor.close()
    if len(q)>0:
        return q[0][0]
    else:
        return None


def storeCache(ex,imgUrl):
    cursor=conn.cursor()
    cursor.execute("""REPLACE INTO 
    cache(file,url,time)
    VALUES (?,?,date('now'))""",(ex,imgUrl))
    conn.commit()
    cursor.close()