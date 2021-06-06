import skyhookConfig, os

if not hasattr(skyhookConfig, 'host'):
    print("[!] IPFS Host is not defined\nPlease modify {}".format(skyhookConfig.__file__))
    exit()
    
if not isinstance(skyhookConfig.host, str):
    print("[!] IPFS Host variable is not a string\nPlease modify {}".format(skyhookConfig.__file__))
    exit()

if not hasattr(skyhookConfig, 'tmpDir'):
    print("[!] Temporary directory is not defined\nPlease modify {}".format(skyhookConfig.__file__))
    exit()
    
if not isinstance(skyhookConfig.tmpDir, str):
    print("[!] Temporary directory variable is not a string\nPlease modify {}".format(skyhookConfig.__file__))
    exit()

if not os.path.isabs(skyhookConfig.tmpDir):
    print("[!] Temporary directory {} is not on an absolute path".format(skyhookConfig.tmpDir))
    exit()

if not (os.access(skyhookConfig.tmpDir, os.W_OK) and os.access(skyhookConfig.tmpDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(skyhookConfig.tmpDir))
    exit()
    
if not hasattr(skyhookConfig, 'skyhookDir'):
    print("[!] Skyhook directory is not defined\nPlease modify {}".format(skyhookConfig.__file__))
    exit()
    
if not isinstance(skyhookConfig.skyhookDir, str):
    print("[!] Skyhook directory variable is not a string\nPlease modify {}".format(skyhookConfig.__file__))
    exit()

if not os.path.isabs(skyhookConfig.skyhookDir):
    print("[!] Skyhook directory {} is not on an absolute path".format(skyhookConfig.skyhookDir))
    exit()
        
if not (os.access(skyhookConfig.skyhookDir, os.W_OK) and os.access(skyhookConfig.skyhookDir, os.R_OK)):
    print("[!] Cannot read or write to and from {}".format(skyhookConfig.skyhookDir))
    exit()
