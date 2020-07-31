import os

# Using infura as to not require the user to run an IPFS node
host = "https://ipfs.infura.io"
port = 5001

# Temporary directory where all the processing happens
tmpDir = "/tmp"

# History location
dbLocation = "{}/.local/skyhook.db".format(os.environ["HOME"])

usage = """
    skyhook clear history   -   Delete everything from history
    skyhook list history    -   List all entries in history
    skyhook list keys       -   List all files and their corresponding encryption keys
    
    skyhook search [file name]  -   Search history for entries matching [file name]
    skyhook delete [hash]       -   Delete an entry specified by [hash] from history
    skyhook save [hash]         -   Save a single history entry specified by [hash] to the current directory (Importable)
    
    skyhook import [path]   -   Import history from a location specified by [path]
    skyhook export [path]   -   Export history to a location specified by [path]
    
    skyhook upload [file name]  -   Upload a file specified by [file name] from the current directory to the IPFS network
    skyhook download [hash]     -   Download a file specified by [hash] from the IPFS network to the current directory
"""
