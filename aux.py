import os, random, string

def cleanUp(filePath):
    os.remove(filePath)

def getRandomString(length):
    return(bytes("".join(random.choice(string.ascii_letters + string.digits) for i in range(length)), "ascii"))