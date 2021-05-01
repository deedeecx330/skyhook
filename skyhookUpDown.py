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
import os, skyhookDb, random, string, skyhookConfig

def getRandomString(length):
    return("".join(random.choice(string.ascii_letters + string.digits) for i in range(length)))

peer = ipfsApi.Client(skyhookConfig.host, skyhookConfig.port)

def uploadFile(fileName):
    currentDir = os.getcwd()
    if not fileName in [f for f in os.listdir(".") if os.path.isfile(f)]:
        return(1)
    else:
        password = getRandomString(32)
        aesName = "{}.sky".format(fileName)
        tmpPath = "{}/{}".format(skyhookConfig.tmpDir.rstrip('/'), aesName)
        print("[+] Encrypting {}".format(fileName))
        try:
            skyhookfilecrypt.encryptFile(fileName, tmpPath, bytes(password, "ascii"))
        except:
            os.remove(tmpPath)
            return(2)
        os.chdir(skyhookConfig.tmpDir)
        print("[+] Uploading {}".format(fileName))
        try:
            result = peer.add(aesName)
            os.chdir(currentDir)
        except:
            os.chdir(currentDir)
            os.remove(tmpPath)
            return(3)
        now = datetime.now()
        currentDate = now.strftime("%d/%m/%Y-%H:%M:%S")
        print("[+] Adding entry to history")
        res = skyhookDb.addToHistory(fileName, result["Hash"], password, currentDate)
        if res == 0:
            pass
        else:
            os.remove(tmpPath)
            return(4)
        os.remove(tmpPath)
        return(0)

def downloadFile(fileHash):
    currentDir = os.getcwd()
    fileName, password = skyhookDb.getEntry(fileHash)
    if fileName == 1 and password == 1:
        return(1)
    saveFile = "{}/{}".format(currentDir, fileName)
    os.chdir(skyhookConfig.tmpDir)
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
        os.remove(fileHash)
        os.chdir(currentDir)
        return(3)
    os.remove(fileHash)
    os.chdir(currentDir)
    return(fileName)
