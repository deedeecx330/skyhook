import skyhookConfig, filecmp, os

if not os.path.isabs(skyhookConfig.skyhookDir):
    print("[!] Skyhook directory {} is not on an absolute path".format(skyhookConfig.skyhookDir))
    exit()
    
if not os.path.isabs(skyhookConfig.configFile):
    print("[!] Configuration file location {} is not on an absolute path".format(skyhookConfig.configFile))
    exit()
    
if not os.path.isabs(skyhookConfig.dbLocation):
    print("[!] History file location {} is not on an absolute path".format(skyhookConfig.dbLocation))
    exit()

if not os.path.isdir(skyhookConfig.skyhookDir):
    try:
        os.makedirs(skyhookConfig.skyhookDir, exist_ok=True)
    except:
        print("[!] Could not create Skyhook directory {}".format(skyhookConfig.skyhookDir))
        exit()
        
if not (os.access(skyhookConfig.skyhookDir, os.W_OK) and os.access(skyhookConfig.skyhookDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(skyhookConfig.skyhookDir))
    exit()
    
if not (os.access(os.path.dirname(skyhookConfig.configFile), os.W_OK) and os.access(os.path.dirname(skyhookConfig.configFile), os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(os.path.dirname(skyhookConfig.configFile)))
    exit()
    
if not (os.access(os.path.dirname(skyhookConfig.dbLocation), os.W_OK) and os.access(os.path.dirname(skyhookConfig.dbLocation), os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(os.path.dirname(skyhookConfig.dbLocation)))
    exit()
        
if not os.path.isfile(skyhookConfig.configFile):
    try:
        os.link(skyhookConfig.__file__, skyhookConfig.configFile)
    except:
        print("[!] Could not create configuration file {}".format(skyhookConfig.configFile))
        exit()
        
if not filecmp.cmp(skyhookConfig.__file__, skyhookConfig.configFile):
    try:
        os.remove(skyhookConfig.configFile)
        os.link(skyhookConfig.__file__, skyhookConfig.configFile)
    except:
        print("[!] Could not create configuration file {}".format(skyhookConfig.configFile))
        exit()
        
if not os.path.isdir(skyhookConfig.tmpDir):
    print("[!] Temporary directory {} is not a valid directory".format(skyhookConfig.tmpDir))
    exit()

if not os.path.isabs(skyhookConfig.tmpDir):
    print("[!] Temporary directory {} is not on an absolute path".format(skyhookConfig.tmpDir))
    exit()

if not (os.access(skyhookConfig.tmpDir, os.W_OK) and os.access(skyhookConfig.tmpDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(skyhookConfig.tmpDir))
    exit()
    
if not hasattr(skyhookConfig, 'configFile'):
    print("[!] Configuration file location is not defined")
    exit()
    
if not isinstance(skyhookConfig.configFile, str):
    print("[!] Configuration file location variable is not a string\nPlease modify {}".format(skyhookConfig.configFile))
    exit()

if not hasattr(skyhookConfig, 'host'):
    print("[!] IPFS Host is not defined\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not isinstance(skyhookConfig.host, str):
    print("[!] IPFS Host variable is not a string\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not hasattr(skyhookConfig, 'port'):
    print("[!] IPFS Port is not defined\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not isinstance(skyhookConfig.port, int):
    print("[!] IPFS Port variable is not an integer\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if skyhookConfig.port < 0 or skyhookConfig.port > 65353:
    print("[!] IPFS Port out of range (0 - 65353)\nPlease modify {}".format(skyhookConfig.configFile))
    exit()

if not hasattr(skyhookConfig, 'tmpDir'):
    print("[!] Temporary directory is not defined\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not isinstance(skyhookConfig.tmpDir, str):
    print("[!] Temporary directory variable is not a string\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not hasattr(skyhookConfig, 'skyhookDir'):
    print("[!] Skyhook directory is not defined\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not isinstance(skyhookConfig.skyhookDir, str):
    print("[!] Skyhook directory variable is not a string\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
    
if not hasattr(skyhookConfig, 'dbLocation'):
    print("[!] Skyhook history file location is not defined")
    exit()
    
if not isinstance(skyhookConfig.dbLocation, str):
    print("[!] Skyhook history file location variable is not a string\nPlease modify {}".format(skyhookConfig.configFile))
    exit()
