import sqlite3, shutil, skyhookConfig
from datetime import datetime
    
dbLocation = "{}/skyhook.db".format(skyhookConfig.skyhookDir.rstrip('/'))
	
try:
    connection = sqlite3.connect(dbLocation)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
except:
    print("[!] Cannot connect to {}".format(dbLocation))
    exit()

def listDb():
    items = cursor.execute("SELECT DISTINCT name, date, hash, key FROM history").fetchall()
    if len(items) == 0:
        return(1)
    else:
        for name, date, hash, key in items:
            print("Name: {} Date: {} Hash: {} Key: {}".format(name, date, hash, key))

def clearDb():
    cursor.execute("DROP TABLE IF EXISTS history")
    connection.commit()
    print("[+] History cleared")

def searchDb(identifier):
    items = cursor.execute("SELECT DISTINCT name, date, hash, key FROM history WHERE hash = ?", (identifier,)).fetchall()
    if len(items) == 0:
        items = cursor.execute("SELECT DISTINCT name, date, hash, key FROM history WHERE name = ?", (identifier,)).fetchall()
    if len(items) == 0:
        return(1)
    else:
        for name, date, hash, key in items:
            print("Name: {} Date: {} Hash: {} Key: {}".format(name, date, hash, key))

def exportDb(newPath):
    try:
        shutil.copyfile(dbLocation, "export.pod")
        return(0)
    except:
        return(1)

def saveOne(identifier):
    items = cursor.execute("SELECT DISTINCT name, hash, key, date FROM history WHERE hash = ?", (identifier,)).fetchall()
    if len(items) == 0:
        items = cursor.execute("SELECT DISTINCT name, hash, key, date FROM history WHERE name = ?", (identifier,)).fetchall()
    if len(items) == 0:
        return(1)
    try:
        auxcon = sqlite3.connect("export.pod")
        auxcur = auxcon.cursor()
        auxcur.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
        for item in items:
            auxcur.execute("INSERT INTO history VALUES (?, ?, ?, ?)", item)
        auxcon.commit()
    except:
        return(2)
    return(0)

def importDb(dbPath):
    try:
        with open(dbPath, "rb") as db:
            header = db.read(15)
    except:
        return(1)
    if header == b"SQLite format 3":
        try:
            auxcon = sqlite3.connect(dbPath)
            auxcur = auxcon.cursor()
            auxfetch = auxcur.execute("SELECT DISTINCT name, hash, key, date FROM history").fetchall()
            if len(auxfetch) == 0:
                return(3)
            else:
                for item in auxfetch:
                    cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", item)
                connection.commit()
                return(0)
        except:
            return(2)
    else:
        return(2) 

def deleteItem(identifier):
    ident = "hash"
    item = cursor.execute("SELECT DISTINCT hash FROM history WHERE hash = ?", (identifier,)).fetchone()
    if item == None:
        item = cursor.execute("SELECT DISTINCT name FROM history WHERE name = ?", (identifier,)).fetchone()
        ident = "name"
    if item == None:
        return(1)
    else:
        try:
            cursor.execute("DELETE FROM history WHERE {} = ?".format(ident), (identifier,))
            connection.commit()
            return(0)
        except:
            return(2)

def getEntry(fileHash):
    try:
        fileName, password = cursor.execute("SELECT DISTINCT name, key FROM history WHERE hash = ?", (fileHash,)).fetchone()
    except:
        return(1, 1)
    return(fileName, password)

def addToHistory(name, hash, key, date):
    try:
        cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (name, hash, key, date,))
        connection.commit()
        return(0)
    except:
        return(1)

def addEntry(name, hash, key):
    if len(hash) != 46:
        return(2)
    if len(key) != 32:
        return(3)
    now = datetime.now()
    currentDate = now.strftime("%d/%m/%Y-%H:%M:%S")
    res = addToHistory(name, hash, key, currentDate)
    return(res)
