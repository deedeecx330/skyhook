try:
    import ipfsApi
except:
    print("Module ipfs-api not installed")
    exit()

import random, string
from datetime import datetime
from crypto import *
from db import *
from config import *

peer = ipfsApi.Client(host, port)

def getRandomString():
    return("".join(random.choice(string.ascii_letters + string.digits) for i in range(32)))

def uploadFile(fileName):

    if not fileName in [f for f in os.listdir('.') if os.path.isfile(f)]:
        return(1)
    else:
        
        password = getRandomString()
        
        aesName = "{}.sky".format(fileName)
        tmpPath = "{}/{}".format(tmpDir, aesName)

        print("[+] Encrypting {}".format(fileName))

        encryptFile(fileName, tmpPath, password)

        os.chdir(tmpDir)
        print("[+] Uploading {}".format(fileName))
        try:
            result = peer.add(aesName)
        except:
            cleanUp(tmpPath)
            return(3)

        now = datetime.now()
        currentDate = now.strftime("%d/%m/%Y %H:%M:%S")
        print("[+] Adding entry to history")
        try:
            cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (fileName, result["Hash"], password, currentDate,))
            connection.commit()
        except:
            cleanUp(tmpPath)
            return(4)

        cleanUp(tmpPath)

        return(0)

def downloadFile(fileHash):

    try:
        fileName, password = cursor.execute("SELECT DISTINCT name, key FROM history WHERE hash = ?", (fileHash,)).fetchone()
    except:
        return(1)

    saveFile = "{}/{}".format(os.getcwd(), fileName)
    os.chdir(tmpDir)
    print("[+] Downloading {}".format(fileName))

    try:
        peer.get(fileHash)
    except:
        return(2)

    print("[+] Decrypting {}".format(fileName))
    try:
        decryptFile(fileHash, saveFile, password)
    except:
        cleanUp(fileHash)
        return(3)

    cleanUp(fileHash)

    return(fileName)