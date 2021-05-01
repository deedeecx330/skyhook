import os, sqlite3, shutil, config
from datetime import datetime

if not os.path.isdir(config.skyhookDir):
    try:
        os.makedirs(config.skyhookDir, exist_ok=True)
    except:
        print("[!] Could not create Skyhook directory {}".format(config.skyhookDir))
        exit()
        
if not (os.access(config.skyhookDir, os.W_OK) and os.access(config.skyhookDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(config.skyhookDir))
    exit()
        
if not os.path.isfile(config.configFile):
    try:
        os.link(config.__file__, config.configFile)
    except:
        print("[!] Could not create configuration file {}".format(config.configFile))
        exit()

if not os.path.isdir(config.tmpDir):
    print("[!] Temporary path {} is not a valid directory".format(config.tmpDir))
    exit()

if not os.path.isabs(config.tmpDir):
    print("[!] Temporary path {} is not absolute".format(config.tmpDir))
    exit()

if not (os.access(config.tmpDir, os.W_OK) and os.access(config.tmpDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(config.tmpDir))
    exit()
    
if not hasattr(config, 'configFile'):
    print("[!] Configuration file location is not defined")
    exit()
    
if not isinstance(config.configFile, str):
    print("[!] Configuration file location variable is not a string\nPlease modify {}".format(config.configFile))
    exit()

if not hasattr(config, 'host'):
    print("[!] IPFS Host is not defined\nPlease modify {}".format(config.configFile))
    exit()
    
if not isinstance(config.host, str):
    print("[!] IPFS Host variable is not a string\nPlease modify {}".format(config.configFile))
    exit()
    
if not hasattr(config, 'port'):
    print("[!] IPFS Port is not defined\nPlease modify {}".format(config.configFile))
    exit()
    
if not isinstance(config.port, int):
    print("[!] IPFS Port variable is not an integer\nPlease modify {}".format(config.configFile))
    exit()
    
if config.port < 0 or config.port > 65353:
    print("[!] IPFS Port out of range (0 - 65353)\nPlease modify {}".format(config.configFile))
    exit()

if not hasattr(config, 'tmpDir'):
    print("[!] Temporary directory is not defined\nPlease modify {}".format(config.configFile))
    exit()
    
if not isinstance(config.tmpDir, str):
    print("[!] Temporary directory variable is not a string\nPlease modify {}".format(config.configFile))
    exit()
    
if not hasattr(config, 'skyhookDir'):
    print("[!] Skyhook directory is not defined\nPlease modify {}".format(config.configFile))
    exit()
    
if not isinstance(config.skyhookDir, str):
    print("[!] Skyhook directory variable is not a string\nPlease modify {}".format(config.configFile))
    exit()
    
if not hasattr(config, 'skyhookDb'):
    print("[!] Skyhook database file location is not defined")
    exit()
    
if not isinstance(config.skyhookDb, str):
    print("[!] Skyhook database file location variable is not a string\nPlease modify {}".format(config.configFile))
    exit()
    
try:
    connection = sqlite3.connect(config.dbLocation)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
except:
    print("[!] Could not connect to {}".format(config.dbLocation))
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
        shutil.copyfile(config.dbLocation, "export.pod")
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
    fileName, password = cursor.execute("SELECT DISTINCT name, key FROM history WHERE hash = ?", (fileHash,)).fetchone()
    if fileName == None or password == None:
        return(1, 1)
    else:
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
