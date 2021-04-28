try:
    import ipfsApi
except:
    print("[!] Module ipfs-api not installed")
    exit()

try:
    import skyhookfilecrypt
except:
    print("[!] Module skyhookfilecrypt not installed")
    exit()

from datetime import datetime
import os, db, aux, config

peer = ipfsApi.Client(config.host, config.port)

def uploadFile(fileName):
    currentDir = os.getcwd()
    if not fileName in [f for f in os.listdir(".") if os.path.isfile(f)]:
        return(1)
    else:
        password = aux.getRandomString(32)
        aesName = "{}.sky".format(fileName)
        tmpPath = "{}/{}".format(config.tmpDir, aesName)
        print("[+] Encrypting {}".format(fileName))
        try:
            skyhookfilecrypt.encryptFile(fileName, tmpPath, bytes(password, "ascii"))
        except:
            aux.cleanUp(tmpPath)
            return(2)
        os.chdir(config.tmpDir)
        print("[+] Uploading {}".format(fileName))
        try:
            result = peer.add(aesName)
            os.chdir(currentDir)
        except:
            os.chdir(currentDir)
            aux.cleanUp(tmpPath)
            return(3)
        now = datetime.now()
        currentDate = now.strftime("%d/%m/%Y-%H:%M:%S")
        print("[+] Adding entry to history")
        res = db.addToHistory(fileName, result["Hash"], password, currentDate)
        if res == 0:
            pass
        else:
            aux.cleanUp(tmpPath)
            return(4)
        aux.cleanUp(tmpPath)
        return(0)

def downloadFile(fileHash):
    currentDir = os.getcwd()
    fileName, password = db.getEntry(fileHash)
    if fileName == 1 and password == 1:
        return(1)
    saveFile = "{}/{}".format(currentDir, fileName)
    os.chdir(config.tmpDir)
    print("[+] Downloading {}".format(fileName))
    try:
        peer.get(fileHash)
    except:
        os.chdir(currentDir)
        return(2)
    print("[+] Decrypting {}".format(fileName))
    try:
        skyhookfilecrypt.decryptFile(fileHash, saveFile, bytes(password, "ascii"))
    except:
        aux.cleanUp(fileHash)
        os.chdir(currentDir)
        return(3)
    aux.cleanUp(fileHash)
    os.chdir(currentDir)
    return(fileName)
