import os, math, threading, multiprocessing
from Crypto.Cipher import AES

separator = b" :><:><:><: "

chunkS = int(math.pow(AES.block_size, 4))
threads = int(math.pow(multiprocessing.cpu_count(), 2))

def pad(content):
    return(content + b"!" * (AES.block_size - len(content) % AES.block_size))

def enCrypt(cipher, content, fileHandle, previous):

    encrypted = cipher.encrypt(content)

    if previous == None:
        fileHandle.write(encrypted)
        exit()
    else:
        while previous.is_alive() == True:
            pass
        else:
            fileHandle.write(encrypted)
            exit()
            
def encryptFile(originalName, newName, key):

    global chunkS
    global threads

    chunkSize = chunkS
    maxThreads = threads

    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    outFile = open(newName, "wb")
    outFile.write(iv + separator)

    inFile = open(originalName, "rb")
    inFile.seek(0, os.SEEK_END)

    contentLength = inFile.tell()

    while contentLength % AES.block_size != 0:
        contentLength = contentLength + 1

    if contentLength <= chunkSize:
        chunkSize = contentLength
        maxThreads = 1

    parts = int(contentLength / chunkSize / maxThreads)

    for i in range(0, parts):

        seekDefault = i * chunkSize * maxThreads

        threadPool = list()
        previous = None
        last = False

        if i == parts - 1:
            last = True
            maxThreads = 1
        
        for x in range(0, maxThreads):

            inFile.seek(seekDefault + x * chunkSize)

            if last == True:
                content = pad(inFile.read())
            else:
                content = inFile.read(chunkSize)

            t = threading.Thread(target=enCrypt, args=(cipher, content, outFile, previous))
            threadPool.append(t)
            previous = t

        for thread in threadPool:
            thread.start()
            thread.join()

        while previous.is_alive() == True:
            pass

    inFile.close()
    outFile.close()

def deCrypt(cipher, content, fileHandle, padded, previous):

    decrypted = cipher.decrypt(content)

    if padded == True:
        decrypted = decrypted.rstrip(b"!")

    if previous == None:
        fileHandle.write(decrypted)
        exit()
    else:
        while previous.is_alive() == True:
            pass
        else:
            fileHandle.write(decrypted)
            exit()

def decryptFile(oldName, newName, key):

    global chunkS
    global threads

    chunkSize = chunkS
    maxThreads = threads

    inFile = open(oldName, "rb")
    outFile = open(newName, "wb")

    iv = inFile.read(16)

    skip = len(iv + separator)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    inFile.seek(0, os.SEEK_END)

    contentLength = inFile.tell() - skip

    if contentLength <= chunkSize:
        chunkSize = contentLength
        maxThreads = 1

    parts = int(contentLength / chunkSize / maxThreads)

    for i in range(0, parts):

        seekDefault = i * chunkSize * maxThreads + skip
        
        threadPool = list()
        previous = None
        last = False
        
        padded = False

        if i == parts - 1:
            last = True
            maxThreads = 1
            padded = True

        for x in range(0, maxThreads):

            inFile.seek(seekDefault + x * chunkSize)

            if last == True:
                content = inFile.read()
            else:
                content = inFile.read(chunkSize)

            t = threading.Thread(target=deCrypt, args=(cipher, content, outFile, padded, previous))
            threadPool.append(t)
            previous = t

        for thread in threadPool:
            thread.start()
            thread.join()

        while previous.is_alive() == True:
            pass

    inFile.close()
    outFile.close()