import os

# Using infura as to not require the user to run an IPFS node
host = "https://ipfs.infura.io"
port = 5001

# Temporary directory where all the processing happens
tmpDir = "/tmp"

# Skyhook directory
skyhookDir = "{}/.local".format(os.environ["HOME"])

# History location
dbLocation = "{}/skyhook.db".format(skyhookDir)

# Configuration file location
dbLocation = "{}/skyhook.config".format(skyhookDir)
