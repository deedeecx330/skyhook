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

    if not fileName in [f for f in os.listdir('.') if os.path.isfile(f)]:
        return(1)
    else:
        
        password = aux.getRandomString(32)
        
        aesName = "{}.sky".format(fileName)
        tmpPath = "{}/{}".format(config.tmpDir, aesName)

        print("[+] Encrypting {}".format(fileName))

        skyhookfilecrypt.encryptFile(fileName, tmpPath, bytes(password, "ascii"))

        os.chdir(config.tmpDir)
        print("[+] Uploading {}".format(fileName))
        try:
            result = peer.add(aesName)
        except:
            aux.cleanUp(tmpPath)
            return(3)

        now = datetime.now()
        currentDate = now.strftime("%d/%m/%Y %H:%M:%S")
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

    fileName, password = db.getEntry(fileHash)

    if fileName == 1 and password == 1:
        return(1)

    saveFile = "{}/{}".format(os.getcwd(), fileName)
    os.chdir(config.tmpDir)
    print("[+] Downloading {}".format(fileName))

    try:
        peer.get(fileHash)
    except:
        return(2)

    print("[+] Decrypting {}".format(fileName))
    try:
        skyhookfilecrypt.decryptFile(fileHash, saveFile, bytes(password, "ascii"))
    except:
        aux.cleanUp(fileHash)
        return(3)

    aux.cleanUp(fileHash)

    return(fileName)