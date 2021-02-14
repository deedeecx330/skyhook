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

    skyhook search [file name/hash]  -   Search history for entries matching [file name/hash]
    skyhook delete [file name/hash]  -   Delete entries specified by [file name/hash] from history
    skyhook save [file name/hash]    -   Save history entries specified by [file name/hash] to the current directory
    skyhook add [name:hash:key]      -	Manually add an entry to history specified by colon-separated values of [name:hash:key]

    skyhook import [path]   -   Import history from a location specified by [path]
    skyhook export [path]   -   Export entire history to a location specified by [path]

    skyhook upload [file name]	-       Upload a file specified by [file name] from the current directory to the IPFS network
    skyhook download [hash]	    -       Download a file specified by [hash] from the IPFS network to the current directory

    It is possible to specify multiple values in a form of a comma-separated list for search,delete,save,import,upload,download and add functions.
"""
