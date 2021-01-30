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
    
    skyhook search [comma-separated list of file names and/or hashes]  -   Search history for entries matching [file names and/or hashes]
    skyhook delete [comma-separated list of file names and/or hashes]  -   Delete entries specified by [file names and/or hashes] from history
    skyhook save [comma-separated list of file names and/or hashes]    -   Save history entries specified by [file names and/or hashes] to the current directory
    
    skyhook import [comma-separated list of paths]   -   Import history from a location specified by [paths]
    skyhook export [path]   -   Export entire history to a location specified by [path]
    
    skyhook upload [comma-separated list of file names]  -   Upload a file specified by [file names] from the current directory to the IPFS network
    skyhook download [comma-separated list of hashes]    -   Download a file specified by [hashes] from the IPFS network to the current directory
"""
