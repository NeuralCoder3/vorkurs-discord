import sqlite3
from sqlite3 import Error

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
    except Error as e:
        print(e)
    return conn

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