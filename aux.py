import os, random, string

def cleanUp(filePath):
    os.remove(filePath)

def getRandomString(length):
    return("".join(random.choice(string.ascii_letters + string.digits) for i in range(length)))