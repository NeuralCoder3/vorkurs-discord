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
    alias TEXT NOT NULL PRIMARY KEY,
    command TEXT NOT NULL
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

def createTables(conn):
    cursor=conn.cursor()
    cursor.execute("")
    conn.commit()
    cursor.close()


# def getField(table,field,condition):
#     global conn
#     conn.execute()
#     conn.commit()
#     pass

# def writeField(table,field,value):
#     cursor=conn.cursor()
#     cursor.execute("REPLACE INTO ?(?)")
#     conn.commit()
#     cursor.close()
#     #     REPLACE INTO table(column_list)
#     # VALUES(value_list);
#     pass

# create_connection("data.db")
