import os, sqlite3, shutil, config

try:
    connection = sqlite3.connect(config.dbLocation)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
except:
    print("[!] Could not connect to {}".format(config.dbLocation))
    exit()

if os.path.isdir(config.tmpDir):
    pass
else:
    print("[!] Temporary path {} is not a valid directory".format(config.tmpDir))
    exit()

if os.path.isabs(config.tmpDir):
    pass
else:
    print("[!] Temporary path {} is not absolute".format(config.tmpDir))
    exit()

if os.access(config.tmpDir, os.W_OK) and os.access(config.tmpDir, os.R_OK):
    pass
else:
    print("[!] Cannot read or write to and from {}".format(config.tmpDir))
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
    items = cursor.execute("SELECT DISTINCT name, date, key FROM history").fetchall()
    if len(items) == 0:
        print("[!] History is empty")
        exit()
    else:
        print("\n[+] Keys (Name (date) [Key])")
        for name, date, key in items:
            print("\n{} ({}) [{}]".format(name, date, key))
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
        shutil.copyfile(config.dbLocation, newPath)
        return(0)
    except:
        return(1)

def saveOne(fileName):
    items = cursor.execute("SELECT DISTINCT name, hash, key, date FROM history WHERE name = ?", (fileName,)).fetchall()
    if len(items) == 0:
        return(1)
    try:
        auxcon = sqlite3.connect("{}.save".format(fileName))
        auxcur = auxcon.cursor()
        auxcur.execute("CREATE TABLE IF NOT EXISTS history (name TEXT, hash TEXT, key TEXT, date TEXT)")
        for item in items:
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

def deleteItem(fileName):
    item = cursor.execute("SELECT DISTINCT name FROM history WHERE name = ?", (fileName,)).fetchone()
    if item == None:
        return(1)
    else:
        try:
            cursor.execute("DELETE FROM history WHERE name = ?", (fileName,))
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