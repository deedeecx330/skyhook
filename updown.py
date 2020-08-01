try:
    import ipfsApi
except:
    print("[!] Module ipfs-api not installed")
    exit()

try:
    from skyhookfilecrypt import *
except:
    print("[!] Module skyhookfilecrypt not installed")
    exit()

from datetime import datetime
from config import *
from db import *
from aux import *

peer = ipfsApi.Client(host, port)

def uploadFile(fileName):

    if not fileName in [f for f in os.listdir('.') if os.path.isfile(f)]:
        return(1)
    else:
        
        password = getRandomString(32)
        
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

        res = addToHistory(fileName, result["Hash"], password, currentDate)
        if res == 0:
            pass
        else:
            cleanUp(tmpPath)
            return(4)

        cleanUp(tmpPath)

        return(0)

def downloadFile(fileHash):

    fileName, password = getEntry(fileHash)

    if fileName == 1 and password == 1:
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