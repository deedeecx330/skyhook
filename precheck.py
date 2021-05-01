import config, filecmp, os

if not os.path.isabs(config.skyhookDir):
    print("[!] Skyhook directory {} is not on an absolute path".format(config.skyhookDir))
    exit()
    
if not os.path.isabs(config.configFile):
    print("[!] Configuration file location {} is not on an absolute path".format(config.configFile))
    exit()
    
if not os.path.isabs(config.dbLocation):
    print("[!] History file location {} is not on an absolute path".format(config.dbLocation))
    exit()

if not os.path.isdir(config.skyhookDir):
    try:
        os.makedirs(config.skyhookDir, exist_ok=True)
    except:
        print("[!] Could not create Skyhook directory {}".format(config.skyhookDir))
        exit()
        
if not (os.access(config.skyhookDir, os.W_OK) and os.access(config.skyhookDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(config.skyhookDir))
    exit()
    
if not (os.access(os.path.dirname(config.configFile), os.W_OK) and os.access(os.path.dirname(config.configFile), os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(os.path.dirname(config.configFile)))
    exit()
    
if not (os.access(os.path.dirname(config.dbLocation), os.W_OK) and os.access(os.path.dirname(config.dbLocation), os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(os.path.dirname(config.dbLocation)))
    exit()
        
if not os.path.isfile(config.configFile):
    try:
        os.link(config.__file__, config.configFile)
    except:
        print("[!] Could not create configuration file {}".format(config.configFile))
        exit()
        
if not filecmp.cmp(config.__file__, config.configFile):
    try:
        os.remove(config.configFile)
        os.link(config.__file__, config.configFile)
    except:
        print("[!] Could not create configuration file {}".format(config.configFile))
        exit()
        
if not os.path.isdir(config.tmpDir):
    print("[!] Temporary directory {} is not a valid directory".format(config.tmpDir))
    exit()

if not os.path.isabs(config.tmpDir):
    print("[!] Temporary directory {} is not on an absolute path".format(config.tmpDir))
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
    
if not hasattr(config, 'dbLocation'):
    print("[!] Skyhook history file location is not defined")
    exit()
    
if not isinstance(config.dbLocation, str):
    print("[!] Skyhook history file location variable is not a string\nPlease modify {}".format(config.configFile))
    exit()
