import os

# Using infura as to not require the user to run an IPFS node
host = "https://ipfs.infura.io"
port = 5001

# Temporary directory where all the processing happens
tmpDir = "/tmp"

# History location
dbLocation = "{}/.local/skyhook.db".format(os.environ["HOME"])
