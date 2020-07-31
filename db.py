import os, sqlite3, shutil
from config import *

try:
    connection = sqlite3.connect(dbLocation)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
except:
    print("[!] Could not connect to {}".format(dbLocation))
    exit()

if os.path.isdir(tmpDir):
    pass
else:
    print("[!] Temporary path {} is not a valid directory".format(tmpDir))
    exit()

if os.path.isabs(tmpDir):
    pass
else:
    print("[!] Temporary path {} is not absolute".format(tmpDir))
    exit()

if os.access(tmpDir, os.W_OK) and os.access(tmpDir, os.R_OK):
    pass
else:
    print("[!] Cannot read or write to and from {}".format(tmpDir))
    exit()

def listDb():
    items = cursor.execute("SELECT DISTINCT name, hash, date FROM history").fetchall()
    if len(items) == 0:
        print("[!] History is empty")
        exit()
    else:
        print("\n[+] History (Name (Date) [Hash])")
        for name, hash, date in items:
            print("\n{} ({}) [{}]".format(name, date, hash))
    print()

def listKeys():
    items = cursor.execute("SELECT DISTINCT name, key FROM history").fetchall()
    if len(items) == 0:
        print("[!] History is empty")
        exit()
    else:
        print("\n[+] Keys (Name [Key])")
        for name, key in items:
            print("\n{} [{}]".format(name, key))
    print()

def clearDb():
    cursor.execute("DROP TABLE IF EXISTS history")
    connection.commit()
    print("[+] History cleared")

def searchDb(fileName):
    items = cursor.execute("SELECT DISTINCT name, hash, date FROM history WHERE name = ?", (fileName,)).fetchall()
    if len(items) == 0:
        print("[!] Could not find any entries for {}".format(fileName))
        exit()
    else:
        print("\n[+] Files (Name (Date) [Hash])")
        for name, hash, date in items:
            print("\n{} ({}) [{}]".format(name, date, hash))
    print()

def exportDb(newPath):
    try:
        shutil.copyfile(dbLocation, newPath)
        return(0)
    except:
        return(1)

def saveOne(fileHash):
    item = cursor.execute("SELECT DISTINCT name, hash, key, date FROM history WHERE hash = ?", (fileHash,)).fetchone()
    if item == None:
        return(1)
    try:
        auxcon = sqlite3.connect("{}.save".format(fileHash))
        auxcur = auxcon.cursor()
        auxcur.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
        auxcur.execute("INSERT INTO history VALUES (?, ?, ?, ?)", tuple(item))
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
                    cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", tuple(item))
                connection.commit()
                return(0)
        except:
            return(2)
    else:
        return(2) 

def deleteItem(fileHash):
    item = cursor.execute("SELECT DISTINCT hash FROM history WHERE hash = ?", (fileHash,)).fetchone()
    if item == None:
        return(1)
    else:
        try:
            cursor.execute("DELETE FROM history WHERE hash = ?", (fileHash,))
            connection.commit()
            return(0)
        except:
            return(2)